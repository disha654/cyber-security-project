from __future__ import annotations

import platform
import subprocess

from .models import Direction, Rule, RuleAction


class IptablesEnforcer:
    """Best-effort Linux-only rule enforcement."""

    def __init__(self) -> None:
        self.supported = platform.system().lower() == "linux"

    def apply_rules(self, rules: list[Rule]) -> list[str]:
        if not self.supported:
            return ["iptables enforcement skipped: only supported on Linux."]

        results: list[str] = []
        for rule in rules:
            if not rule.enabled:
                continue
            command = self._build_command(rule)
            if not command:
                results.append(f"Skipped rule '{rule.name}': insufficient fields for iptables.")
                continue
            try:
                subprocess.run(command, check=True, capture_output=True, text=True)
                results.append(f"Applied rule '{rule.name}'.")
            except subprocess.CalledProcessError as exc:
                results.append(f"Failed rule '{rule.name}': {exc.stderr.strip() or exc.stdout.strip()}")
        return results

    def _build_command(self, rule: Rule) -> list[str] | None:
        if rule.action not in {RuleAction.ALLOW, RuleAction.BLOCK}:
            return None

        chain = "INPUT" if rule.direction == Direction.INBOUND else "OUTPUT"
        target = "ACCEPT" if rule.action == RuleAction.ALLOW else "DROP"
        command = ["iptables", "-A", chain]

        if rule.protocol:
            command.extend(["-p", rule.protocol.lower()])
        if rule.src_ip:
            command.extend(["-s", rule.src_ip])
        if rule.dst_ip:
            command.extend(["-d", rule.dst_ip])
        if rule.src_port is not None:
            command.extend(["--sport", str(rule.src_port)])
        if rule.dst_port is not None:
            command.extend(["--dport", str(rule.dst_port)])
        command.extend(["-j", target])
        return command
