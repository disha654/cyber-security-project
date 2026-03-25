from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .app import FirewallApplication
from .models import Direction, Rule, RuleAction


class FirewallMonitorGUI:
    def __init__(self, app: FirewallApplication):
        self.app = app
        self.root = tk.Tk()
        self.root.title("Personal Firewall Monitor")
        self.root.geometry("980x520")
        self._build()
        self.app.subscribe(self._on_packet)

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            frame,
            columns=("time", "action", "src", "dst", "proto", "ports", "rule"),
            show="headings",
            height=16,
        )
        for key, title, width in (
            ("time", "Time", 190),
            ("action", "Action", 80),
            ("src", "Source", 140),
            ("dst", "Destination", 140),
            ("proto", "Protocol", 80),
            ("ports", "Ports", 120),
            ("rule", "Rule", 170),
        ):
            self.tree.heading(key, text=title)
            self.tree.column(key, width=width, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        controls = ttk.LabelFrame(frame, text="Quick Rule", padding=10)
        controls.pack(fill=tk.X, pady=(12, 0))

        self.name_var = tk.StringVar(value="block-host")
        self.ip_var = tk.StringVar()
        self.port_var = tk.StringVar()
        self.proto_var = tk.StringVar(value="tcp")
        self.action_var = tk.StringVar(value=RuleAction.BLOCK.value)

        for idx, (label, variable) in enumerate(
            (
                ("Name", self.name_var),
                ("IP", self.ip_var),
                ("Port", self.port_var),
                ("Protocol", self.proto_var),
                ("Action", self.action_var),
            )
        ):
            ttk.Label(controls, text=label).grid(row=0, column=idx * 2, sticky=tk.W, padx=(0, 6))
            widget = ttk.Entry(controls, textvariable=variable, width=16)
            if label in {"Protocol", "Action"}:
                values = ["tcp", "udp", "icmp"] if label == "Protocol" else [item.value for item in RuleAction]
                widget = ttk.Combobox(controls, textvariable=variable, values=values, state="readonly", width=14)
            widget.grid(row=0, column=idx * 2 + 1, padx=(0, 12))

        ttk.Button(controls, text="Add Rule", command=self._add_rule).grid(row=0, column=10, padx=(8, 0))
        ttk.Button(controls, text="Apply iptables", command=self._apply_iptables).grid(row=0, column=11, padx=(8, 0))

    def _on_packet(self, packet, action, rule) -> None:
        ports = f"{packet.src_port or '-'}->{packet.dst_port or '-'}"
        self.root.after(
            0,
            lambda: self.tree.insert(
                "",
                0,
                values=(
                    packet.timestamp,
                    action.value,
                    packet.src_ip,
                    packet.dst_ip,
                    packet.protocol,
                    ports,
                    rule.name if rule else "default_policy",
                ),
            ),
        )

    def _add_rule(self) -> None:
        port = int(self.port_var.get()) if self.port_var.get().strip() else None
        rule = Rule(
            name=self.name_var.get().strip(),
            action=RuleAction(self.action_var.get()),
            direction=Direction.ANY,
            src_ip=self.ip_var.get().strip() or None,
            protocol=self.proto_var.get().strip() or None,
            dst_port=port,
            description="Added from GUI",
        )
        self.app.add_rule(rule)
        messagebox.showinfo("Rule Added", f"Rule '{rule.name}' saved.")

    def _apply_iptables(self) -> None:
        results = "\n".join(self.app.enforce_rules())
        messagebox.showinfo("iptables", results or "No rules were applied.")

    def run(self) -> None:
        self.root.mainloop()
