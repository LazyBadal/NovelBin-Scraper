import os
from epub_builder import build_epub

def main():
    folder = input("Enter folder path (e.g. data/Supreme Harem God System): ").strip()

    if not os.path.exists(folder):
        print("[ERROR] Folder does not exist.")
        return

    book_title = os.path.basename(folder)

    build_epub(folder, book_title)

if __name__ == "__main__":
    main()