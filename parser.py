from bs4 import BeautifulSoup

def parse_chapter(html):

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    content_div = soup.find(
        "div",
        id="chr-content"
    )

    if not content_div:
        return "Unknown Chapter", ""

    # Title
    title_tag = soup.find("h2")

    chapter_title = (
        title_tag.get_text(strip=True)
        if title_tag else "Unknown Chapter"
    )

    # Remove junk
    for junk in content_div.find_all([
        "script",
        "style",
        "iframe",
        "ins",
        "ads",
        "noscript"
    ]):
        junk.decompose()

    # Convert <br> to newlines
    for br in content_div.find_all("br"):
        br.replace_with("\n")

    chapter_text = content_div.get_text(
        separator="\n",
        strip=True
    )

    # Cleanup excessive empty lines
    lines = []

    for line in chapter_text.splitlines():

        line = line.strip()

        if not line:
            continue

        lines.append(line)

    chapter_text = "\n\n".join(lines)

    return chapter_title, chapter_text