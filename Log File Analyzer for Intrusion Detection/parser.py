import re
import pandas as pd
from datetime import datetime

def parse_apache_log(file_path):
    """Parses Apache access logs."""
    apache_regex = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<url>.*?) HTTP/.*?" (?P<status>\d+) (?P<size>\d+|-)'
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            match = re.search(apache_regex, line)
            if match:
                entry = match.groupdict()
                # Parse timestamp: 25/Mar/2026:10:00:01 +0000
                entry['timestamp'] = datetime.strptime(entry['timestamp'].split()[0], '%d/%b/%Y:%H:%M:%S')
                entry['status'] = int(entry['status'])
                data.append(entry)
    return pd.DataFrame(data)

def parse_ssh_log(file_path):
    """Parses SSH auth logs."""
    ssh_regex = r'(?P<timestamp>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+.*?\ssshd\[\d+\]:\s+(?P<message>.*)'
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            match = re.search(ssh_regex, line)
            if match:
                entry = match.groupdict()
                # Extract IP from message
                ip_match = re.search(r'from (?P<ip>\d+\.\d+\.\d+\.\d+)', entry['message'])
                entry['ip'] = ip_match.group('ip') if ip_match else 'unknown'
                
                # Determine event type
                if 'Failed password' in entry['message']:
                    entry['event'] = 'Failed Login'
                elif 'Accepted password' in entry['message']:
                    entry['event'] = 'Successful Login'
                elif 'Invalid user' in entry['message']:
                    entry['event'] = 'Invalid User'
                else:
                    entry['event'] = 'Other'
                
                # Parse timestamp (Year is missing in SSH logs, assuming current year)
                current_year = datetime.now().year
                entry['timestamp'] = datetime.strptime(f"{current_year} {entry['timestamp']}", '%Y %b %d %H:%M:%S')
                data.append(entry)
    return pd.DataFrame(data)
