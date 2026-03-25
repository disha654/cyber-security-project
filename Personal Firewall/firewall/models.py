from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from ipaddress import ip_address
from typing import Any


class RuleAction(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"


class Direction(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    ANY = "any"


@dataclass(slots=True)
class PacketInfo:
    timestamp: str
    direction: Direction
    src_ip: str
    dst_ip: str
    protocol: str
    src_port: int | None = None
    dst_port: int | None = None
    length: int = 0
    summary: str = ""


@dataclass(slots=True)
class Rule:
    name: str
    action: RuleAction
    direction: Direction = Direction.ANY
    src_ip: str | None = None
    dst_ip: str | None = None
    protocol: str | None = None
    src_port: int | None = None
    dst_port: int | None = None
    enabled: bool = True
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def matches(self, packet: PacketInfo) -> bool:
        if not self.enabled:
            return False
        if self.direction != Direction.ANY and packet.direction != self.direction:
            return False
        if self.protocol and packet.protocol.lower() != self.protocol.lower():
            return False
        if self.src_ip and not self._ip_matches(packet.src_ip, self.src_ip):
            return False
        if self.dst_ip and not self._ip_matches(packet.dst_ip, self.dst_ip):
            return False
        if self.src_port is not None and packet.src_port != self.src_port:
            return False
        if self.dst_port is not None and packet.dst_port != self.dst_port:
            return False
        return True

    @staticmethod
    def _ip_matches(actual: str, expected: str) -> bool:
        try:
            return ip_address(actual) == ip_address(expected)
        except ValueError:
            return actual == expected
