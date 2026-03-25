from __future__ import annotations

import platform
from datetime import datetime, timezone
from threading import Event
from typing import Callable

from .models import Direction, PacketInfo

try:
    from scapy.all import IP, TCP, UDP, get_if_list, sniff  # type: ignore[import-untyped]
    if platform.system().lower() == "windows":
        from scapy.arch.windows import get_windows_if_list  # type: ignore[import-untyped]
    else:  # pragma: no cover - platform-specific
        get_windows_if_list = None
except ModuleNotFoundError:  # pragma: no cover - depends on environment
    IP = TCP = UDP = get_if_list = sniff = None
    get_windows_if_list = None


class PacketSniffer:
    def __init__(self, interface: str | None = None, packet_count: int = 0):
        self.interface = interface
        self.packet_count = packet_count
        self._stop_event = Event()
        self.last_error: RuntimeError | None = None

    def ensure_ready(self) -> None:
        if sniff is None:
            raise RuntimeError("Scapy is not installed. Run 'pip install -r requirements.txt' first.")

    def available_interfaces(self) -> list[str]:
        self.ensure_ready()
        if platform.system().lower() == "windows" and get_windows_if_list is not None:
            try:
                interfaces = []
                for adapter in get_windows_if_list():
                    guid = adapter.get("guid", "")
                    pcap_name = f"\\Device\\NPF_{guid}" if guid else ""
                    ips = ", ".join(adapter.get("ips", [])) or "no IPs"
                    name = adapter.get("name") or "Unknown"
                    description = adapter.get("description") or "No description"
                    interfaces.append(f"{name} | {description} | {ips} | use: {pcap_name}")
                return interfaces
            except Exception:
                return []
        try:
            return list(get_if_list()) if get_if_list is not None else []
        except Exception:
            return []

    def start(
        self,
        callback: Callable[[PacketInfo], None],
        bpf_filter: str | None = None,
        error_callback: Callable[[RuntimeError], None] | None = None,
    ) -> None:
        self.ensure_ready()
        self.last_error = None

        def process(packet) -> None:
            info = self._packet_to_info(packet)
            if info:
                callback(info)

        try:
            sniff(
                iface=self.interface,
                prn=process,
                filter=bpf_filter,
                store=False,
                count=self.packet_count,
                stop_filter=lambda _: self._stop_event.is_set(),
            )
        except Exception as exc:
            error = RuntimeError(self._format_sniff_error(exc))
            self.last_error = error
            if error_callback is not None:
                error_callback(error)
                return
            raise error

    def stop(self) -> None:
        self._stop_event.set()

    @staticmethod
    def _packet_to_info(packet) -> PacketInfo | None:
        if IP is None or IP not in packet:
            return None

        ip_layer = packet[IP]
        direction = Direction.OUTBOUND if ip_layer.src.startswith(("10.", "172.", "192.168.")) else Direction.INBOUND
        protocol = str(ip_layer.proto)
        src_port = None
        dst_port = None

        if TCP in packet:
            protocol = "tcp"
            src_port = int(packet[TCP].sport)
            dst_port = int(packet[TCP].dport)
        elif UDP in packet:
            protocol = "udp"
            src_port = int(packet[UDP].sport)
            dst_port = int(packet[UDP].dport)

        return PacketInfo(
            timestamp=datetime.now(timezone.utc).isoformat(),
            direction=direction,
            src_ip=str(ip_layer.src),
            dst_ip=str(ip_layer.dst),
            protocol=protocol,
            src_port=src_port,
            dst_port=dst_port,
            length=len(packet),
            summary=packet.summary(),
        )

    @staticmethod
    def _format_sniff_error(exc: Exception) -> str:
        message = str(exc).strip() or exc.__class__.__name__
        if platform.system().lower() == "windows":
            return (
                "Packet capture failed on Windows. Make sure Npcap is installed, run the terminal as Administrator, "
                "and choose a valid adapter with --interface or the list-interfaces command. "
                f"Original error: {message}"
            )
        return f"Packet capture failed: {message}"
