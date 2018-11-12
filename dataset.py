

def parse_gutenberg(
    text,
    FIRST_CONTENT_LINE_LENGTH=300,
    remove=["Produced by", "End of the Project Gutenberg", "End of Project Gutenberg"],
):
    """
    Reads a raw Project Gutenberg etext, reformat paragraphs,
    and removes fluff.Determines the title of the book 

    Modified from https://github.com/motoom/gutenberg-ebook-scraping/blob/master/gutenberg.py
    """

    lines = [line.strip() for line in text.split("\n")]
    collect = False
    lookforsubtitle = False
    outlines = []
    startseen = endseen = False
    found_first_paragraph = False
    title = ""
    author = ""
    language = ""
    extra = []
    for line in lines:
        if line.startswith("Author: "):
            author = line[8:]
        if line.startswith("Language: "):
            language = line[10:]
        if line.startswith("Title: "):
            title = line[7:]
            lookforsubtitle = True
            continue
        if lookforsubtitle:
            if not line.strip():
                lookforsubtitle = False
            else:
                subtitle = line.strip()
                subtitle = subtitle.strip(".")
                title += ", " + subtitle
        if (
            ("*** START" in line)
            or ("***START" in line)
            or (line.startswith("*END THE SMALL PRINT!"))
        ):
            collect = startseen = True
            paragraph = ""
            extra.append(line)
            continue

        if ("*** END" in line) or ("***END" in line):
            endseen = True
            extra.append(line)
            break
        if not collect:
            extra.append(line)
            continue
        if not line:
            paragraph = paragraph.strip().replace("_", "")
            for term in remove:
                if paragraph.startswith(term):
                    extra.append(line)
                    paragraph = ""
                    break
            # Skip all the misc paragraphs, and only start at the first long paragraphs
            if not found_first_paragraph:
                if len(paragraph) > FIRST_CONTENT_LINE_LENGTH:
                    found_first_paragraph = True
            if paragraph and found_first_paragraph:
                outlines.append(paragraph)
                outlines.append("")
            paragraph = ""
        else:
            paragraph += " " + line

    # Report on anomalous situations, but don't make it a showstopper.
    if not title:
        print("    Problem: No title found\n")
    if not startseen:
        print("    Problem: No '*** START' seen\n")
    if not endseen:
        print("    Problem: No '*** END' seen\n")

    return dict(
        content="\n".join(outlines),
        title=title,
        author=author,
        language=language,
        extra=extra,
    )
