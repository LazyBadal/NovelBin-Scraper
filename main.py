import os
import time
import random
from datetime import datetime

from scraper import fetch_page, create_session
from parser import parse_chapter
from saver import save_chapter
from toc_loader import load_all_chapters


def write_log(log_path, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def download_novel(
    url,
    start,
    end,
    progress_callback=None,
    status_callback=None
):

    url = url.split("#")[0]

    chapters = load_all_chapters(url)

    if not chapters:
        raise Exception("No chapters found.")

    if start < 1 or end > len(chapters) or start > end:
        raise Exception("Invalid chapter range.")

    selected_chapters = chapters[start - 1:end]

    base_dir = os.path.dirname(os.path.abspath(__file__))

    slug = (
    url.rstrip("/")
    .split("/")[-1]
    .split("#")[0]
)

    novel_folder = slug.replace("-", " ").title()

    folder_name = os.path.join(base_dir, "data", novel_folder)

    os.makedirs(folder_name, exist_ok=True)

    log_path = os.path.join(folder_name, "download_log.txt")

    failed_log_path = os.path.join(folder_name, "failed_chapters.txt")

    if os.path.exists(failed_log_path):
        os.remove(failed_log_path)

    write_log(log_path, "\n" + "=" * 50)
    write_log(log_path, "NEW RUN")
    write_log(log_path, f"URL: {url}")
    write_log(log_path, f"Range: {start} -> {end}")
    write_log(log_path, "=" * 50)

    session = create_session(url)

    failed_chapters = []

    saved_count = 0

    total = len(selected_chapters)

    for idx, chapter in enumerate(selected_chapters, start=1):

        chapter_num = start + idx - 1

        short_msg = f"{chapter_num:04d} - {chapter['title']}"

        if status_callback:
            status_callback(short_msg)

        if progress_callback:
            progress_callback(idx, total)

        write_log(log_path, f"STARTED: {short_msg}")

        html = fetch_page(session, chapter["url"])

        if not html:
            failed_chapters.append(
                (chapter_num, chapter["title"], "fetch_failed")
            )

            write_log(log_path, f"FAILED: {short_msg} (fetch_failed)")

            continue

        title, text = parse_chapter(html)

        if not text.strip():
            failed_chapters.append(
                (chapter_num, chapter["title"], "empty_content")
            )

            write_log(log_path, f"FAILED: {short_msg} (empty_content)")

            continue

        save_chapter(folder_name, chapter_num, title, text)

        saved_count += 1

        write_log(log_path, f"SAVED: {chapter_num:04d} - {title}")

        delay = random.uniform(2.5, 4.5)

        write_log(log_path, f"SLEEP: {delay:.2f}s")

        time.sleep(delay)

        if chapter_num % 25 == 0:

            long_break = random.uniform(20.0, 35.0)

            write_log(
                log_path,
                f"LONG BREAK: {long_break:.2f}s after chapter {chapter_num:04d}"
            )

            time.sleep(long_break)

    if failed_chapters:

        with open(failed_log_path, "w", encoding="utf-8") as f:

            for num, title, reason in failed_chapters:

                line = f"{num:04d} - {title} ({reason})"

                f.write(line + "\n")

                write_log(log_path, line)

    write_log(
        log_path,
        f"SUMMARY: Saved={saved_count}, Failed={len(failed_chapters)}"
    )

    write_log(log_path, "Download run finished.")

    return {
        "saved": saved_count,
        "failed": len(failed_chapters),
        "folder": folder_name
    }


def main():

    url = input("Enter NovelBin URL: ").strip()

    try:
        start = int(input("Start chapter number: "))

        end = int(input("End chapter number: "))

    except ValueError:

        print("[ERROR] Please enter valid numbers.")

        return

    result = download_novel(url, start, end)

    print("\nDone.")

    print(f"Saved: {result['saved']}")

    print(f"Failed: {result['failed']}")

    print(f"Folder: {result['folder']}")


if __name__ == "__main__":
    main()