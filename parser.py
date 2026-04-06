from bs4 import BeautifulSoup

def parse_chapter(html):
    soup = BeautifulSoup(html, "lxml")

    title_tag = soup.find("h3", class_="chapter-title")
    content_div = soup.find("div", id="chr-content")

    chapter_title = title_tag.get_text(strip=True) if title_tag else "Unknown Chapter"

    if not content_div:
        return chapter_title, ""

    paragraphs = content_div.find_all("p")
    chapter_text = "\n".join(
        p.get_text(strip=True)
        for p in paragraphs
        if p.get_text(strip=True)
    )

    return chapter_title, chapter_text