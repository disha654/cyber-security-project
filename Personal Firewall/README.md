# Personal Firewall in Python

This project implements a lightweight personal firewall for cyber security coursework. It uses `scapy` to inspect packets, a JSON ruleset to allow or block traffic, audit logging for suspicious activity, and an optional Tkinter dashboard for live monitoring. On Linux, the same rules can be pushed to `iptables` for system-level enforcement.

## Features

- Packet sniffing with `scapy`
- Rule-based allow and block decisions for IPs, ports, protocols, and direction
- JSON audit logging for packet events
- CLI for running the firewall and adding rules
- Optional Tkinter GUI for live monitoring and quick rule creation
- Optional Linux `iptables` enforcement hook

## Project Layout

- `main.py`: CLI entry point
- `firewall/app.py`: Orchestrates sniffing, rules, logging, and subscribers
- `firewall/sniffer.py`: Converts packets into normalized packet metadata
- `firewall/rules.py`: Loads, saves, and evaluates firewall rules
- `firewall/enforcer.py`: Best-effort `iptables` rule application on Linux
- `firewall/gui.py`: Optional Tkinter monitoring window
- `rules.json`: Sample rules

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On Linux/macOS, activate the environment with `source .venv/bin/activate`.

## Run The Firewall

```bash
python main.py --rules rules.json --log logs/firewall_audit.log
```

Optional flags:

- `--interface <name>`: capture on a specific interface
- `--filter "tcp or udp"`: pass a BPF filter to `scapy`
- `--gui`: launch the Tkinter monitor
- `--apply-iptables`: apply current rules to `iptables` on Linux

## Add A Rule

```bash
python main.py add-rule --name block-ssh --action block --direction inbound --protocol tcp --dst-port 22
```

## GUI

```bash
python main.py --gui
```

The GUI shows live packet decisions and lets you quickly add an IP/port rule. Packet sniffing still requires the privileges expected by `scapy`.

## Notes

- Packet capture often requires administrator or root privileges.
- `iptables` support is Linux-only.
- On Windows, this project still works as a packet monitor, rule engine, and logger, but it does not enforce `iptables`.
- The packet direction heuristic is lightweight and based on private-address detection. For a production firewall, bind direction to actual host interfaces and routing state.
