import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch: {url}")
        print(e)
        return None