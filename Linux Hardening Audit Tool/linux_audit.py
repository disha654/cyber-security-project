#!/usr/bin/env python3
"""
Linux Hardening Audit Tool
This script audits a Linux system's security configuration based on CIS Benchmarks.
It checks for:
- File permissions on critical files
- SSH configuration settings
- Network security parameters (sysctl)
- Firewall status
- Common rootkit indicators
- Unused/vulnerable services
"""

import os
import subprocess
import json
import platform
import stat
import re
from datetime import datetime

class AuditCheck:
    def __init__(self, name, category, description):
        self.name = name
        self.category = category
        self.description = description
        self.status = "PENDING"
        self.details = ""
        self.recommendation = ""

class SecurityAuditor:
    def __init__(self):
        self.checks = []
        self.total_checks = 0
        self.passed_checks = 0

    def add_check(self, name, category, description):
        check = AuditCheck(name, category, description)
        self.checks.append(check)
        return check

    def run_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip(), result.returncode
        except Exception as e:
            return str(e), -1

    def check_file_permissions(self, path, expected_mode, expected_owner="root", expected_group="root"):
        check = self.add_check(f"Permission check for {path}", "Filesystem", f"Verify {path} has mode {oct(expected_mode)}")
        
        if not os.path.exists(path):
            check.status = "NOT FOUND"
            check.details = f"File {path} does not exist."
            return

        try:
            st = os.stat(path)
            actual_mode = stat.S_IMODE(st.st_mode)
            import pwd, grp
            actual_owner = pwd.getpwuid(st.st_uid).pw_name
            actual_group = grp.getgrgid(st.st_gid).gr_name

            if actual_mode == expected_mode and actual_owner == expected_owner:
                check.status = "PASS"
                check.details = f"Mode: {oct(actual_mode)}, Owner: {actual_owner}, Group: {actual_group}"
                self.passed_checks += 1
            else:
                check.status = "FAIL"
                check.details = f"Actual: Mode {oct(actual_mode)}, Owner {actual_owner}. Expected: {oct(expected_mode)}, {expected_owner}"
                check.recommendation = f"chmod {oct(expected_mode)} {path}; chown {expected_owner}:{expected_group} {path}"
        except Exception as e:
            check.status = "ERROR"
            check.details = str(e)

    def check_ssh_config(self, parameter, expected_value):
        check = self.add_check(f"SSH Config: {parameter}", "SSH", f"Verify {parameter} is set to {expected_value}")
        config_path = "/etc/ssh/sshd_config"
        
        if not os.path.exists(config_path):
            check.status = "NOT FOUND"
            check.details = f"SSH config not found at {config_path}"
            return

        try:
            with open(config_path, 'r') as f:
                content = f.read()
                # Match parameter at start of line (case-insensitive)
                pattern = rf"^\s*{parameter}\s+(['\"]?)(.+?)(\1)\s*$"
                match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
                
                if match:
                    actual_value = match.group(2).lower()
                    if actual_value == expected_value.lower():
                        check.status = "PASS"
                        check.details = f"Found {parameter} = {actual_value}"
                        self.passed_checks += 1
                    else:
                        check.status = "FAIL"
                        check.details = f"Found {parameter} = {actual_value}, expected {expected_value}"
                        check.recommendation = f"Update {parameter} to {expected_value} in {config_path}"
                else:
                    check.status = "FAIL"
                    check.details = f"{parameter} not explicitly set"
                    check.recommendation = f"Add '{parameter} {expected_value}' to {config_path}"
        except Exception as e:
            check.status = "ERROR"
            check.details = str(e)

    def check_sysctl(self, param, expected_value):
        check = self.add_check(f"Kernel Param: {param}", "Network", f"Verify {param} is {expected_value}")
        val, code = self.run_command(f"sysctl -n {param}")
        
        if code == 0:
            if val == expected_value:
                check.status = "PASS"
                check.details = f"Value is {val}"
                self.passed_checks += 1
            else:
                check.status = "FAIL"
                check.details = f"Value is {val}, expected {expected_value}"
                check.recommendation = f"sysctl -w {param}={expected_value}"
        else:
            check.status = "ERROR"
            check.details = val

    def check_firewall(self):
        check = self.add_check("Firewall Status", "Network", "Verify if UFW or Iptables is active")
        ufw_status, code = self.run_command("ufw status")
        if "Status: active" in ufw_status:
            check.status = "PASS"
            check.details = "UFW is active"
            self.passed_checks += 1
            return

        iptables_status, code = self.run_command("iptables -L -n")
        if code == 0 and len(iptables_status.split('\n')) > 3: # Basic check for rules
            check.status = "PASS"
            check.details = "Iptables has active rules"
            self.passed_checks += 1
        else:
            check.status = "FAIL"
            check.details = "No active firewall detected (UFW/Iptables)"
            check.recommendation = "Enable UFW: sudo ufw enable"

    def check_rootkit_indicators(self):
        check = self.add_check("Rootkit Indicators", "Security", "Check for common rootkit files")
        suspicious_paths = [
            "/usr/include/... ", "/usr/include/.. ", "/usr/lib/.. ", 
            "/dev/.udev", "/dev/.static", "/dev/.init"
        ]
        found = []
        for p in suspicious_paths:
            if os.path.exists(p):
                found.append(p)
        
        if not found:
            check.status = "PASS"
            check.details = "No common rootkit paths found"
            self.passed_checks += 1
        else:
            check.status = "FAIL"
            check.details = f"Found suspicious paths: {', '.join(found)}"
            check.recommendation = "Investigate the system for potential compromise using 'rkhunter' or 'chkrootkit'."

    def check_unused_services(self):
        check = self.add_check("Unused Services", "Services", "Check for common vulnerable services")
        vulnerable = ["telnet", "rsh", "ftp", "tftp", "talk"]
        active = []
        for svc in vulnerable:
            status, code = self.run_command(f"systemctl is-active {svc}")
            if status == "active":
                active.append(svc)
        
        if not active:
            check.status = "PASS"
            check.details = "No known vulnerable services active"
            self.passed_checks += 1
        else:
            check.status = "FAIL"
            check.details = f"Active vulnerable services: {', '.join(active)}"
            check.recommendation = f"Disable services: sudo systemctl stop {' '.join(active)} && sudo systemctl disable {' '.join(active)}"

    def run_all(self):
        self.check_file_permissions("/etc/shadow", 0o000)
        self.check_file_permissions("/etc/passwd", 0o644)
        self.check_file_permissions("/etc/group", 0o644)
        self.check_file_permissions("/etc/gshadow", 0o000)
        
        self.check_ssh_config("PermitRootLogin", "no")
        self.check_ssh_config("PasswordAuthentication", "no")
        self.check_ssh_config("MaxAuthTries", "4")
        
        self.check_sysctl("net.ipv4.ip_forward", "0")
        self.check_sysctl("net.ipv4.conf.all.send_redirects", "0")
        self.check_sysctl("net.ipv4.conf.all.accept_redirects", "0")
        
        self.check_firewall()
        self.check_rootkit_indicators()
        self.check_unused_services()

    def generate_report(self):
        score = (self.passed_checks / len(self.checks)) * 100 if self.checks else 0
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "os": platform.platform(),
            "compliance_score": f"{score:.2f}%",
            "results": []
        }
        
        for c in self.checks:
            report["results"].append({
                "check": c.name,
                "category": c.category,
                "status": c.status,
                "details": c.details,
                "recommendation": c.recommendation
            })
        
        return report

def print_text_report(report):
    print("="*60)
    print("        LINUX HARDENING AUDIT REPORT")
    print("="*60)
    print(f"Timestamp: {report['timestamp']}")
    print(f"OS:        {report['os']}")
    print(f"Score:     {report['compliance_score']}")
    print("-" * 60)
    
    for res in report["results"]:
        status_color = ""
        if res["status"] == "PASS":
            status_color = "[PASS]"
        elif res["status"] == "FAIL":
            status_color = "[FAIL]"
        else:
            status_color = f"[{res['status']}]"
            
        print(f"{status_color:<8} {res['category']:<12} {res['check']}")
        if res["status"] != "PASS":
            print(f"         Details: {res['details']}")
            if res["recommendation"]:
                print(f"         Fix:     {res['recommendation']}")
        print("-" * 60)

if __name__ == "__main__":
    if platform.system() != "Linux":
        print("Warning: This tool is designed for Linux systems.")
        print("Current OS detected:", platform.system())
        print("Attempting to run checks (some will fail on Windows)...\n")
    
    auditor = SecurityAuditor()
    auditor.run_all()
    report = auditor.generate_report()
    
    print_text_report(report)
    
    # Save to JSON
    with open("audit_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print("\nDetailed JSON report saved to audit_report.json")
