import argparse

from .create_anki_deck_file import DEFAULT_ANKI_DECK_FILENAME, create_anki_deck_file
from .scrape_mdn_css_properties_docs import DEFAULT_MDN_DOCS_JSON_FILENAME, scrape_css_properties_info_from_mdn


def cli():
    parser = argparse.ArgumentParser(description=("Scrape CSS properties info from MDN and save it to a JSON file"))
    parser.add_argument(
        "--css-properties-output-file",
        dest="css_properties_info_output_filename",
        default=DEFAULT_MDN_DOCS_JSON_FILENAME,
        type=str,
        help=(
            "Path to the JSON file where CSS properties info will be saved (default: "
            f"'{DEFAULT_MDN_DOCS_JSON_FILENAME}')"
        ),
    )
    parser.add_argument(
        "--anki-deck-output-file",
        dest="anki_deck_output_filename",
        default=DEFAULT_ANKI_DECK_FILENAME,
        type=str,
        help=f"Output file for the Anki deck (default: '{DEFAULT_ANKI_DECK_FILENAME}')",
    )
    args = parser.parse_args()

    scrape_css_properties_info_from_mdn(args.css_properties_info_output_filename)
    create_anki_deck_file(
        args.css_properties_info_output_filename,
        args.anki_deck_output_filename,
    )


if __name__ == "__main__":
    cli()
