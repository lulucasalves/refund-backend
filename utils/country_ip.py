import requests


def get_country_from_ip(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=country")
        data = response.json()
        if data.get("country"):
            if data["country"] == "Brazil":
                return "BR"

            return "US"
        else:
            return "US"
    except Exception:
        return "US"
