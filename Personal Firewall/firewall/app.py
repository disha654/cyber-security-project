from __future__ import annotations

import threading
from collections import deque
from pathlib import Path
from typing import Callable

from .enforcer import IptablesEnforcer
from .logging_utils import configure_logging, log_packet_event
from .models import PacketInfo, Rule, RuleAction
from .rules import RuleSet
from .sniffer import PacketSniffer


class FirewallApplication:
    def __init__(self, rules_path: str, log_path: str, interface: str | None = None):
        self.rules_path = Path(rules_path)
        self.log_path = Path(log_path)
        self.rules = RuleSet.from_file(self.rules_path)
        self.logger = configure_logging(self.log_path)
        self.sniffer = PacketSniffer(interface=interface)
        self.enforcer = IptablesEnforcer()
        self.packet_history: deque[tuple[PacketInfo, RuleAction, Rule | None]] = deque(maxlen=200)
        self._subscribers: list[Callable[[PacketInfo, RuleAction, Rule | None], None]] = []
        self._thread: threading.Thread | None = None
        self._runtime_error: RuntimeError | None = None

    def start(self, bpf_filter: str | None = None) -> None:
        self.sniffer.ensure_ready()
        self._runtime_error = None
        self._thread = threading.Thread(
            target=self.sniffer.start,
            kwargs={
                "callback": self.handle_packet,
                "bpf_filter": bpf_filter,
                "error_callback": self._record_runtime_error,
            },
            daemon=True,
        )
        self._thread.start()
        self._thread.join(timeout=0.5)
        if self._runtime_error is not None:
            raise self._runtime_error

    def stop(self) -> None:
        self.sniffer.stop()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

    def reload_rules(self) -> None:
        self.rules = RuleSet.from_file(self.rules_path)

    def save_rules(self) -> None:
        self.rules.to_file(self.rules_path)

    def handle_packet(self, packet: PacketInfo) -> None:
        action, rule = self.rules.evaluate(packet)
        self.packet_history.appendleft((packet, action, rule))
        log_packet_event(self.logger, packet, action, rule)
        for subscriber in self._subscribers:
            subscriber(packet, action, rule)

    def subscribe(self, callback: Callable[[PacketInfo, RuleAction, Rule | None], None]) -> None:
        self._subscribers.append(callback)

    def add_rule(self, rule: Rule) -> None:
        self.rules.add_rule(rule)
        self.save_rules()

    def enforce_rules(self) -> list[str]:
        return self.enforcer.apply_rules(self.rules.rules)

    def available_interfaces(self) -> list[str]:
        return self.sniffer.available_interfaces()

    @property
    def runtime_error(self) -> RuntimeError | None:
        return self._runtime_error

    def _record_runtime_error(self, error: RuntimeError) -> None:
        self._runtime_error = error
