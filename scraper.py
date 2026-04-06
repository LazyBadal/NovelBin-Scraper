import requests

def create_session(base_url):
    session = requests.Session()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/146.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-GB,en;q=0.7",
        "Referer": base_url,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    session.headers.update(headers)

    # Prime cookies/session by visiting the main novel page
    try:
        response = session.get(base_url, timeout=15)
        print(f"[INFO] Session primed with main page: {response.status_code}")
    except requests.RequestException as e:
        print("[WARNING] Could not prime session.")
        print(e)

    return session

def fetch_page(session, url):
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch: {url}")
        print(e)
        return None