import requests
from bs4 import BeautifulSoup


def load_all_chapters(url):

    clean_url = url.split("#")[0].strip().rstrip("/")

    slug = clean_url.split("/")[-1]

    archive_url = (
        "https://novelbin.me/ajax/"
        f"chapter-archive?novelId={slug}"
    )

    print(f"[INFO] Fetching archive: {archive_url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/146.0.0.0 Safari/537.36"
        ),
        "X-Requested-With": "XMLHttpRequest",
        "Referer": clean_url
    }

    session = requests.Session()

    response = session.get(
        archive_url,
        headers=headers
    )

    print(f"[INFO] Status: {response.status_code}")

    if response.status_code != 200:

        print("[ERROR] Failed to fetch chapter archive")

        return []

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    chapter_elements = soup.select("a")

    chapters = []

    seen = set()

    for el in chapter_elements:

        href = el.get("href")

        if not href:
            continue

        if href.startswith("/"):
            href = "https://novelbin.me" + href

        if href in seen:
            continue

        seen.add(href)

        title = (
            el.get("title", "").strip()
            or el.get_text(strip=True)
        )

        chapters.append({
            "title": title,
            "url": href
        })

    print(f"[INFO] Found {len(chapters)} chapters")

    return chapters
