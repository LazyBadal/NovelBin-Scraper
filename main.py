import os
import time

from scraper import fetch_page, create_session
from parser import parse_chapter
from saver import save_chapter
from toc_loader import load_all_chapters


def main():
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

    # Save inside project folder -> data/<Novel Name>/
    base_dir = os.path.dirname(os.path.abspath(__file__))
    slug = url.split("/b/")[-1].split("#")[0].strip("/")
    novel_folder = slug.replace("-", " ").title()
    folder_name = os.path.join(base_dir, "data", novel_folder)

    # Shared browser-like session
    session = create_session(url)

    failed_chapters = []

    for i, chapter in enumerate(selected_chapters, start=start):
        print(f"[INFO] Downloading Chapter {i}: {chapter['title']}")

        html = fetch_page(session, chapter["url"])
        if not html:
            failed_chapters.append((i, chapter["title"], "fetch_failed"))
            continue

        title, text = parse_chapter(html)

        if not text.strip():
            print(f"[WARNING] Empty content: {title}")
            failed_chapters.append((i, chapter["title"], "empty_content"))
            continue

        save_chapter(folder_name, i, title, text)

        time.sleep(1.5)

    # Final summary
    if failed_chapters:
        print("\n[SUMMARY] Failed chapters:")
        for num, title, reason in failed_chapters:
            print(f"{num:04d} - {title} ({reason})")

        log_path = os.path.join(folder_name, "failed_chapters.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            for num, title, reason in failed_chapters:
                f.write(f"{num:04d} - {title} ({reason})\n")

        print(f"[INFO] Failure log saved to: {log_path}")
    else:
        print("\n[SUMMARY] All chapters downloaded successfully.")


if __name__ == "__main__":
    main()