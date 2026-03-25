import requests

# Example of a public blacklist source (Firehol blocklist)
BLOCKLIST_URLS = [
    "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset"
]

def get_public_blacklist():
    """Fetches a small sample of blocked IPs (Mocking for efficiency)."""
    # For demonstration, we'll return a static set of mock malicious IPs
    return {"192.168.1.10", "192.168.1.100", "10.0.0.1"}

def check_blacklist(df):
    """Flags IPs in the dataframe that are in the blacklist."""
    if df.empty:
        return pd.DataFrame()
    blacklist = get_public_blacklist()
    return df[df['ip'].isin(blacklist)]
