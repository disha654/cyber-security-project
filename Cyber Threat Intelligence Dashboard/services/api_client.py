import requests
import os
from dotenv import load_dotenv

load_dotenv()

class CTIClient:
    def __init__(self):
        self.vt_api_key = os.getenv("VIRUSTOTAL_API_KEY")
        self.abuse_api_key = os.getenv("ABUSEIPDB_API_KEY")

    def lookup_ip_virustotal(self, ip):
        if not self.vt_api_key:
            return {"error": "VirusTotal API Key missing"}
        
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {"x-apikey": self.vt_api_key}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                attributes = data.get("data", {}).get("attributes", {})
                last_analysis_stats = attributes.get("last_analysis_stats", {})
                return {
                    "source": "VirusTotal",
                    "reputation": attributes.get("reputation", 0),
                    "malicious_count": last_analysis_stats.get("malicious", 0),
                    "suspicious_count": last_analysis_stats.get("suspicious", 0),
                    "harmless_count": last_analysis_stats.get("harmless", 0),
                    "undetermined_count": last_analysis_stats.get("undetermined", 0),
                    "asn": attributes.get("asn", "N/A"),
                    "as_owner": attributes.get("as_owner", "N/A"),
                    "country": attributes.get("country", "N/A")
                }
            else:
                return {"error": f"VirusTotal Error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def lookup_ip_abuseipdb(self, ip):
        if not self.abuse_api_key:
            return {"error": "AbuseIPDB API Key missing"}

        url = "https://api.abuseipdb.com/api/v2/check"
        params = {
            "ipAddress": ip,
            "maxAgeInDays": "90"
        }
        headers = {
            "Accept": "application/json",
            "Key": self.abuse_api_key
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json().get("data", {})
                return {
                    "source": "AbuseIPDB",
                    "abuse_confidence_score": data.get("abuseConfidenceScore", 0),
                    "total_reports": data.get("totalReports", 0),
                    "last_reported_at": data.get("lastReportedAt", "N/A"),
                    "domain": data.get("domain", "N/A"),
                    "usage_type": data.get("usageType", "N/A")
                }
            else:
                return {"error": f"AbuseIPDB Error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def lookup_domain_virustotal(self, domain):
        if not self.vt_api_key:
            return {"error": "VirusTotal API Key missing"}

        url = f"https://www.virustotal.com/api/v3/domains/{domain}"
        headers = {"x-apikey": self.vt_api_key}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                attributes = data.get("data", {}).get("attributes", {})
                last_analysis_stats = attributes.get("last_analysis_stats", {})
                return {
                    "source": "VirusTotal",
                    "reputation": attributes.get("reputation", 0),
                    "malicious_count": last_analysis_stats.get("malicious", 0),
                    "suspicious_count": last_analysis_stats.get("suspicious", 0),
                    "harmless_count": last_analysis_stats.get("harmless", 0),
                    "undetermined_count": last_analysis_stats.get("undetermined", 0),
                    "whois": attributes.get("whois", "N/A")[:500], # Truncate for display
                    "categories": attributes.get("categories", {})
                }
            else:
                return {"error": f"VirusTotal Error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
