from bs4 import BeautifulSoup

def parse_chapter(html):
    soup = BeautifulSoup(html, "lxml")

    content_div = soup.find("div", id="chr-content")

    if not content_div:
        return "Unknown Chapter", ""

    # Find the real chapter title inside content
    title_tag = content_div.find("h3")
    chapter_title = title_tag.get_text(strip=True) if title_tag else "Unknown Chapter"

    # Remove junk tags we don't want
    for junk in content_div.find_all(["script", "style", "iframe"]):
        junk.decompose()

    chapter_lines = []
    started = False

    for tag in content_div.find_all(["h3", "p"]):
        if tag.name == "h3":
            started = True
            continue

        if not started:
            continue

        text = tag.get_text(strip=True)

        # Skip empty junk
        if not text:
            continue

        chapter_lines.append(text)

    chapter_text = "\n\n".join(chapter_lines)

    return chapter_title, chapter_text