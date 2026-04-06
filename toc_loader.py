import requests
from bs4 import BeautifulSoup

def load_all_chapters(url):
    clean_url = url.split("#")[0].strip().rstrip("/")

    if "/b/" in clean_url:
        slug = clean_url.split("/b/")[-1]
    elif "novelId=" in clean_url:
        slug = clean_url.split("novelId=")[-1]
    else:
        print("[ERROR] Could not extract novel slug from URL.")
        return []

    archive_url = f"https://novelbin.com/ajax/chapter-archive?novelId={slug}"
    print(f"[INFO] Fetching chapter archive: {archive_url}")

    session = requests.Session()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/146.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.7",
        "Referer": f"https://novelbin.com/b/{slug}",
        "X-Requested-With": "XMLHttpRequest",
    }

    # First hit main page to get cookies
    main_page = session.get(f"https://novelbin.com/b/{slug}", headers=headers)
    print(f"[INFO] Main page status: {main_page.status_code}")

    # Then hit AJAX archive endpoint
    response = session.get(archive_url, headers=headers)
    print(f"[INFO] Archive page status: {response.status_code}")

    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch archive page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    chapter_elements = soup.select("ul.list-chapter li a")

    chapters = []
    seen = set()

    for el in chapter_elements:
        title = el.get("title", "").strip() or el.get_text(strip=True)
        href = el.get("href")

        if href and href not in seen:
            seen.add(href)
            chapters.append({
                "title": title if title else "Unknown Chapter",
                "url": href
            })

    return chapters