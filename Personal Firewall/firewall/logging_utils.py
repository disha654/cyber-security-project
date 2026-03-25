from __future__ import annotations

import json
import logging
from pathlib import Path

from .models import PacketInfo, Rule, RuleAction


def configure_logging(log_path: str | Path) -> logging.Logger:
    logger = logging.getLogger("personal_firewall")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger

    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    return logger


def log_packet_event(logger: logging.Logger, packet: PacketInfo, action: RuleAction, rule: Rule | None) -> None:
    entry = {
        "timestamp": packet.timestamp,
        "action": action.value,
        "rule": rule.name if rule else "default_policy",
        "direction": packet.direction.value,
        "src_ip": packet.src_ip,
        "dst_ip": packet.dst_ip,
        "protocol": packet.protocol,
        "src_port": packet.src_port,
        "dst_port": packet.dst_port,
        "length": packet.length,
        "summary": packet.summary,
    }
    logger.info(json.dumps(entry))
