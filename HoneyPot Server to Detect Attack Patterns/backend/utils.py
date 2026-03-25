import requests

def get_geolocation(ip):
    if ip == "127.0.0.1" or ip == "localhost":
        # Mock data for localhost
        return {
            "city": "Localhost",
            "country": "Internal",
            "lat": 0.0,
            "lon": 0.0
        }
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data["status"] == "success":
            return {
                "city": data.get("city"),
                "country": data.get("country"),
                "lat": data.get("lat"),
                "lon": data.get("lon")
            }
    except Exception as e:
        print(f"Error fetching geolocation: {e}")
    
    return {
        "city": "Unknown",
        "country": "Unknown",
        "lat": 0.0,
        "lon": 0.0
    }
