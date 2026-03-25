from __future__ import annotations

import argparse
import sys
import time

from firewall import FirewallApplication
from firewall.gui import FirewallMonitorGUI
from firewall.models import Direction, Rule, RuleAction


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lightweight personal firewall using Scapy.")
    parser.add_argument("--rules", default="rules.json", help="Path to the firewall rules JSON file.")
    parser.add_argument("--log", default="logs/firewall_audit.log", help="Path to the audit log file.")
    parser.add_argument("--interface", default=None, help="Network interface for sniffing.")
    parser.add_argument("--filter", default=None, help="Optional BPF filter.")
    parser.add_argument("--gui", action="store_true", help="Launch the Tkinter live monitor.")
    parser.add_argument("--apply-iptables", action="store_true", help="Apply current rules using iptables on Linux.")

    subparsers = parser.add_subparsers(dest="command")

    add_rule = subparsers.add_parser("add-rule", help="Add a rule to the ruleset.")
    add_rule.add_argument("--name", required=True)
    add_rule.add_argument("--action", required=True, choices=[item.value for item in RuleAction])
    add_rule.add_argument("--direction", default=Direction.ANY.value, choices=[item.value for item in Direction])
    add_rule.add_argument("--src-ip")
    add_rule.add_argument("--dst-ip")
    add_rule.add_argument("--protocol")
    add_rule.add_argument("--src-port", type=int)
    add_rule.add_argument("--dst-port", type=int)
    add_rule.add_argument("--description", default="")

    subparsers.add_parser("list-interfaces", help="List interfaces available to Scapy.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    app = FirewallApplication(rules_path=args.rules, log_path=args.log, interface=args.interface)

    if args.command == "add-rule":
        rule = Rule(
            name=args.name,
            action=RuleAction(args.action),
            direction=Direction(args.direction),
            src_ip=args.src_ip,
            dst_ip=args.dst_ip,
            protocol=args.protocol,
            src_port=args.src_port,
            dst_port=args.dst_port,
            description=args.description,
        )
        app.add_rule(rule)
        print(f"Added rule '{rule.name}' to {args.rules}")
        return 0

    if args.command == "list-interfaces":
        try:
            interfaces = app.available_interfaces()
        except RuntimeError as exc:
            print(f"Interface listing failed: {exc}", file=sys.stderr)
            return 1
        if not interfaces:
            print("No interfaces were returned by Scapy.")
            return 1
        for interface in interfaces:
            print(interface)
        return 0

    if args.apply_iptables:
        for result in app.enforce_rules():
            print(result)

    if args.gui:
        try:
            app.start(bpf_filter=args.filter)
            gui = FirewallMonitorGUI(app)
            gui.run()
        except RuntimeError as exc:
            print(f"Startup failed: {exc}", file=sys.stderr)
            return 1
        finally:
            app.stop()
        return 0

    try:
        app.start(bpf_filter=args.filter)
    except RuntimeError as exc:
        print(f"Startup failed: {exc}", file=sys.stderr)
        return 1

    print("Firewall is running. Press Ctrl+C to stop.")
    try:
        while True:
            if app.runtime_error is not None:
                print(f"\nCapture stopped: {app.runtime_error}", file=sys.stderr)
                return 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping firewall...")
    finally:
        app.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
