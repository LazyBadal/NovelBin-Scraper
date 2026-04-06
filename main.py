from scraper import fetch_page, create_session
from parser import parse_chapter
from saver import save_chapter
from toc_loader import load_all_chapters
import time

def main():
    novel_name = input("Enter Novel Name: ")
    url = input("Enter NovelBin URL: ").strip()
    url = url.split("#")[0]

    chapters = load_all_chapters(url)

    if not chapters:
        print("[ERROR] No chapters found.")
        return

    print(f"[INFO] Found {len(chapters)} chapters")
    for ch in chapters[:5]:
        print(ch)

    try:
        start = int(input("Start chapter number: "))
        end = int(input("End chapter number: "))
    except ValueError:
        print("[ERROR] Please enter valid numbers.")
        return

    if start < 1 or end > len(chapters) or start > end:
        print("[ERROR] Invalid range.")
        return

    selected_chapters = chapters[start - 1:end]
    folder_name = novel_name

    # Create one shared session for all chapter downloads
    session = create_session(url)

    for i, chapter in enumerate(selected_chapters, start=start):
        print(f"[INFO] Downloading Chapter {i}: {chapter['title']}")

        html = fetch_page(session, chapter["url"])
        if not html:
            continue

        title, text = parse_chapter(html)

        if text.strip():
            save_chapter(folder_name, i, title, text)
        else:
            print(f"[WARNING] Empty content: {title}")

        time.sleep(1.5)

if __name__ == "__main__":
    main()