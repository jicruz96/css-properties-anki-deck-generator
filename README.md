# **CSS Properties Anki Deck** | (Download [Here](https://ankiweb.net/shared/info/1468761769))

This repository contains a text file of Anki cards for ~all~ most* CSS properties listed in the [MDN Web Docs CSS Properties Reference](https://developer.mozilla.org/en-US/docs/Web/CSS), as well as the original scripts used to generate the deck.

> _*Deprecated and experimental properties are currently **NOT** included._


## Download

#### **RECOMMENDED:** Download the official deck from AnkiWeb's shared decks [**here**](https://ankiweb.net/shared/info/1468761769).

_Alternatively, download [**CSS-PROPERTIES-ANKI-DECK.txt**](./CSS-PROPERTIES-ANKI-DECK.txt) and import it into Anki. Note that it will be up to you to format the deck yourself._

## Contributing

> :wave: **Contributions welcome!**

The MDN scraper isn't perfect and the MDN docs are always getting updated, so you're welcome to contribute to the project by:

  * improving the MDN Docs scraping script or the Anki Deck generator script.
  * rerunning the scraper and updating the Anki Deck file.

In either case, please open an issue or a pull request and I'll be happy to help you out.

### Prerequisites

* Python 3.11+
* [Poetry](https://python-poetry.org/) package manager

### Setup & Usage

1. Clone the repository and `cd` into it.
2. Install the dependencies with `poetry install` and activate the virtual environment with `poetry shell`.
3. Run the scripts as needed like so:

```bash
poetry install
poetry shell

# this command will scrape the MDN CSS properties docs and save the output to a file
scrape_mdn_css_properties_docs --output-file data/mdn-css-properties-info.json

# this command will create an Anki deck file from the scraped MDN data
create_anki_deck_file --input-file data/mdn-css-properties-info.json --output-file css-properties-anki-deck.txt

# you can also run this command to combine the previous two commands:
scrape_mdn_and_create_deck --css-properties-output-file data/mdn-css-properties-info.json --anki-deck-output-file css-properties-anki-deck.txt
```
