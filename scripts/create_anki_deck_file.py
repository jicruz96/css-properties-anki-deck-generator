import argparse
import csv
import json
import os

from tqdm import tqdm

from .scrape_mdn_css_properties_docs import DEFAULT_MDN_DOCS_JSON_FILENAME

DEFAULT_ANKI_DECK_FILENAME = "NEW-CSS-PROPERTIES-ANKI-DECK.txt"
ANKI_DECK_COLUMN_NAMES = [
    "front",
    "back",
    "url",
    "extra_info",
    "formal_definition",
    "syntax",
    "see_also",
    "tag",
]
ANKI_DECK_HEADER = f"""\
#separator:Pipe
#html:true
#deck:CSS properties (typed)
#notetype:type-in
#columns:{'|'.join(ANKI_DECK_COLUMN_NAMES)}
#tags column:{ANKI_DECK_COLUMN_NAMES.index("tag")}
"""


def create_anki_deck_file(
    css_properties_info_filename: str,
    anki_deck_filename: str,
):
    if os.path.exists(anki_deck_filename):
        raise FileExistsError(f"{anki_deck_filename} already exists. This script will not overwrite it.")

    # load the CSS properties info from the JSON file
    with open(css_properties_info_filename, "r") as fp:
        css_properties_info_list = json.load(fp)

    # create each row of the Anki deck
    rows = []
    for css_property_info in tqdm(css_properties_info_list):
        # breakpoint()
        row = create_flash_card_row(css_property_info)
        rows.append(row)

    # write the Anki deck to a file
    with open(anki_deck_filename, "w") as fp:
        fp.write(ANKI_DECK_HEADER)
    with open(anki_deck_filename, "a", newline="") as fp:
        writer = csv.writer(fp, delimiter="|", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)


def create_flash_card_row(css_property_info: dict[str, str]) -> list[str]:
    front, extra_info = css_property_info["main_description"].split(".", maxsplit=1)
    extras = [css_property_info.get(key, "") for key in ["formal_definition", "syntax", "see_also", "tag"]]
    row = [
        front,  # the front of the card is the first sentence describing the CSS property
        css_property_info["name"],  # the back of the card is the CSS property name
        css_property_info["url"],  # the URL of the MDN page for the CSS property is the 3rd column of the file.
        extra_info,  # the extra info is the rest of CSS property description
        *extras,  # the rest of the columns are the formal definition, syntax, see also, and tag fields
    ]
    row = [format_text(text) for text in row]
    return row


def format_text(text: str) -> str:
    # replace newlines with <br> tags for Anki
    return text.replace("\n", "<br>")


def cli():
    parser = argparse.ArgumentParser(
        description=(
            "Generate Anki flashcard deck from the CSS properties info JSON file produced by the command "
            "scrape_mdn_css_properties_docs"
        )
    )
    parser.add_argument(
        "--input-file",
        dest="input_file",
        type=str,
        default=DEFAULT_MDN_DOCS_JSON_FILENAME,
        help=f"Path to the JSON file containing the CSS properties info (default: '{DEFAULT_MDN_DOCS_JSON_FILENAME}')",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default=DEFAULT_ANKI_DECK_FILENAME,
        help=f"Output file for the Anki deck (default: '{DEFAULT_ANKI_DECK_FILENAME}')",
    )
    args = parser.parse_args()

    create_anki_deck_file(
        css_properties_info_filename=args.input_file,
        anki_deck_filename=args.output_file,
    )


if __name__ == "__main__":
    cli()
