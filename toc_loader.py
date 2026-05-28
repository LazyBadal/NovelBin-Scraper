import requests
from bs4 import BeautifulSoup


def load_all_chapters(url):

    clean_url = url.split("#")[0].strip().rstrip("/")

    slug = clean_url.split("/")[-1]

    archive_url = (
        "https://novelbin.me/ajax/"
        f"chapter-archive?novelId={slug}"
    )

    print(f"[INFO] Fetching chapter archive: {archive_url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/146.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.7",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": clean_url,
    }

    response = requests.get(
        archive_url,
        headers=headers
    )

    print(f"[INFO] Archive status: {response.status_code}")

    if response.status_code != 200:

        print(
            f"[ERROR] Failed to fetch archive: "
            f"{response.status_code}"
        )

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
            "title": title if title else "Unknown Chapter",
            "url": href
        })

    print(f"[INFO] Found {len(chapters)} chapters")

    return chapters
