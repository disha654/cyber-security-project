import parser
import analyzer
import blacklist
import visualizer
import pandas as pd
import os

def main():
    print("Starting Log File Analyzer...")
    
    # 1. Parse Logs
    print("Parsing logs...")
    apache_df = parser.parse_apache_log('logs/apache_access.log')
    ssh_df = parser.parse_ssh_log('logs/ssh_auth.log')
    
    # 2. Analyze Data
    print("Analyzing data...")
    
    # Brute Force
    brute_force = analyzer.detect_brute_force(ssh_df)
    if not brute_force.empty:
        print(f"[ALERT] Detected {len(brute_force['ip'].unique())} IPs attempting Brute Force.")
        brute_force.to_csv('reports/brute_force_alerts.csv', index=False)
    
    # DoS
    dos_attempts = analyzer.detect_dos(apache_df)
    if not dos_attempts.empty:
        print(f"[ALERT] Detected {len(dos_attempts['ip'].unique())} IPs with DoS-like behavior.")
        dos_attempts.to_csv('reports/dos_alerts.csv', index=False)
        
    # Scanning
    scanning_attempts = analyzer.detect_scanning(apache_df)
    if not scanning_attempts.empty:
        print(f"[ALERT] Detected {len(scanning_attempts['ip'].unique())} IPs scanning for vulnerabilities.")
        scanning_attempts.to_csv('reports/scanning_alerts.csv', index=False)

    # Blacklist Check
    print("Checking blacklists...")
    malicious_apache = blacklist.check_blacklist(apache_df)
    malicious_ssh = blacklist.check_blacklist(ssh_df)
    
    if not malicious_apache.empty:
         print(f"[ALERT] Found {len(malicious_apache['ip'].unique())} Blacklisted IPs in Apache logs.")
         malicious_apache.to_csv('reports/blacklisted_apache.csv', index=False)
         
    if not malicious_ssh.empty:
         print(f"[ALERT] Found {len(malicious_ssh['ip'].unique())} Blacklisted IPs in SSH logs.")
         malicious_ssh.to_csv('reports/blacklisted_ssh.csv', index=False)

    # 3. Visualize
    print("Generating visualizations...")
    visualizer.plot_top_ips(apache_df, 'Top Source IPs (Apache)', 'top_ips_apache.png')
    visualizer.plot_methods(apache_df, 'HTTP Method Distribution', 'top_methods_apache.png')
    
    if not ssh_df.empty:
         visualizer.plot_top_ips(ssh_df, 'Top Source IPs (SSH)', 'top_ips_ssh.png')

    print("Analysis Complete. Check 'reports/' directory.")

if __name__ == "__main__":
    main()
