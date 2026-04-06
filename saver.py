import os

def sanitize_filename(name):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, "")
    return name.strip()

import os

def sanitize_filename(name):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, "")
    return name.strip()

def save_chapter(folder_name, chapter_number, chapter_title, chapter_text):
    os.makedirs(folder_name, exist_ok=True)

    safe_title = sanitize_filename(chapter_title)
    file_name = f"{chapter_number:04d} - {safe_title}.txt"
    file_path = os.path.join(folder_name, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(chapter_title + "\n\n")
        f.write(chapter_text)

    print(f"[SAVED] {file_path}")