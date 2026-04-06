from ebooklib import epub
import os
import html

def txt_to_html_paragraphs(text):
    paragraphs = text.split("\n")
    return "\n".join(
        f"<p>{html.escape(p.strip())}</p>"
        for p in paragraphs
        if p.strip()
    )

def build_epub(folder_path, book_title, author="Unknown Author"):
    book = epub.EpubBook()

    # Metadata
    book.set_identifier(book_title.lower().replace(" ", "-"))
    book.set_title(book_title)
    book.set_language("en")
    book.add_author(author)

    chapter_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    )

    epub_chapters = []

    for file_name in chapter_files:
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        if not lines:
            continue

        raw_title = lines[0].strip()

        # Extract chapter number from filename prefix like "0002 - ..."
        chapter_number = file_name.split(" - ")[0]
        chapter_title = f"{chapter_number} - {raw_title}"

        chapter_text = "\n".join(lines[2:]).strip() if len(lines) > 2 else ""

        chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=f"chap_{chapter_number}.xhtml",
            lang="en"
        )

        chapter.content = f"""
        <h1>{html.escape(chapter_title)}</h1>
        {txt_to_html_paragraphs(chapter_text)}
        """

        book.add_item(chapter)
        epub_chapters.append(chapter)

    # TOC
    book.toc = tuple(epub_chapters)

    # Navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Basic CSS
    style = """
    body {
        font-family: serif;
        line-height: 1.6;
        margin: 5%;
    }
    h1 {
        text-align: center;
        margin-bottom: 1.5em;
    }
    p {
        text-indent: 1.5em;
        margin-top: 0.5em;
        margin-bottom: 0.5em;
    }
    """

    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style
    )

    book.add_item(nav_css)

    # Spine
    book.spine = ["nav"] + epub_chapters

    output_path = os.path.join(folder_path, f"{book_title}.epub")
    epub.write_epub(output_path, book, {})

    print(f"[EPUB SAVED] {output_path}")