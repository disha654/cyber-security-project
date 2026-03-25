import pandas as pd

def detect_brute_force(df, threshold=5):
    """Detects brute-force based on failed SSH logins."""
    if df.empty or 'event' not in df.columns:
        return pd.DataFrame()
    failed_logins = df[df['event'] == 'Failed Login']
    counts = failed_logins.groupby('ip').size()
    brute_force_ips = counts[counts >= threshold].index.tolist()
    return failed_logins[failed_logins['ip'].isin(brute_force_ips)]

def detect_dos(df, threshold=10, time_window='1s'):
    """Detects DoS based on request frequency (Apache)."""
    if df.empty or 'timestamp' not in df.columns:
        return pd.DataFrame()
    df = df.set_index('timestamp')
    dos_alerts = []
    for ip, group in df.groupby('ip'):
        # Resample by time window and count requests
        counts = group.resample(time_window).size()
        if any(counts >= threshold):
            dos_alerts.append(ip)
    return df[df['ip'].isin(dos_alerts)].reset_index()

def detect_scanning(df, threshold=5):
    """Detects scanning based on status codes (404/403) or multiple unique URLs (Apache)."""
    if df.empty:
        return pd.DataFrame()
    # IPs with high count of 401, 403, 404
    scanning_ips = df[df['status'].isin([401, 403, 404])].groupby('ip').size()
    scanning_ips = scanning_ips[scanning_ips >= threshold].index.tolist()
    return df[df['ip'].isin(scanning_ips)]
