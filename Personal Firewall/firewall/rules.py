from __future__ import annotations

import json
from pathlib import Path

from .models import Direction, PacketInfo, Rule, RuleAction


class RuleSet:
    def __init__(self, rules: list[Rule] | None = None, default_action: RuleAction = RuleAction.ALLOW):
        self.rules = rules or []
        self.default_action = default_action

    @classmethod
    def from_file(cls, path: str | Path) -> "RuleSet":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        default_action = RuleAction(payload.get("default_action", RuleAction.ALLOW.value))
        rules = [cls._build_rule(item) for item in payload.get("rules", [])]
        return cls(rules=rules, default_action=default_action)

    def to_file(self, path: str | Path) -> None:
        payload = {
            "default_action": self.default_action.value,
            "rules": [self._serialize_rule(rule) for rule in self.rules],
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def evaluate(self, packet: PacketInfo) -> tuple[RuleAction, Rule | None]:
        for rule in self.rules:
            if rule.matches(packet):
                return rule.action, rule
        return self.default_action, None

    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    @staticmethod
    def _build_rule(item: dict) -> Rule:
        return Rule(
            name=item["name"],
            action=RuleAction(item["action"]),
            direction=Direction(item.get("direction", Direction.ANY.value)),
            src_ip=item.get("src_ip"),
            dst_ip=item.get("dst_ip"),
            protocol=item.get("protocol"),
            src_port=item.get("src_port"),
            dst_port=item.get("dst_port"),
            enabled=item.get("enabled", True),
            description=item.get("description", ""),
            metadata=item.get("metadata", {}),
        )

    @staticmethod
    def _serialize_rule(rule: Rule) -> dict:
        return {
            "name": rule.name,
            "action": rule.action.value,
            "direction": rule.direction.value,
            "src_ip": rule.src_ip,
            "dst_ip": rule.dst_ip,
            "protocol": rule.protocol,
            "src_port": rule.src_port,
            "dst_port": rule.dst_port,
            "enabled": rule.enabled,
            "description": rule.description,
            "metadata": rule.metadata,
        }
