import argparse
import json
import os

import requests
from bs4 import BeautifulSoup, Tag
from rich import print
from tqdm import tqdm

DEFAULT_MDN_DOCS_JSON_FILENAME = "data/mdn-css-properties-info.json"


def get_syntax_section(soup: BeautifulSoup) -> str:
    syntax_section = soup.find("section", attrs={"aria-labelledby": "syntax"})
    code_text = soup.find("pre").text
    rest_of_section = syntax_section.find("div", class_="section-content")
    code_section = rest_of_section.find("div", class_="code-example")
    if code_section:
        code_section.replace_with("")
    return f"<pre>\n{code_text}\n</pre>\n" + rest_of_section.decode_contents()


def get_formal_definition(soup: BeautifulSoup) -> str:
    return (
        soup.find("section", attrs={"aria-labelledby": "formal_definition"})
        .find("table", class_="properties")
        .decode_contents()
    )


def get_see_also(soup: BeautifulSoup) -> str:
    return (
        soup.find("section", attrs={"aria-labelledby": "see_also"})
        .find("div", class_="section-content")
        .decode_contents()
    )


def get_constituent_properties(soup: BeautifulSoup) -> str:
    return (
        soup.find("section", attrs={"aria-labelledby": "constituent_properties"})
        .find("div", class_="section-content")
        .decode_contents()
    )


def get_try_it(soup: BeautifulSoup) -> str:
    return ",".join(
        child.text
        for child in soup.find("section", attrs={"aria-labelledby": "try_it"})
        .find("div", class_="section-content")
        .children
        if child.name != "iframe"
    )


def get_description(soup: BeautifulSoup) -> str:
    return soup.find("section", attrs={"aria-labelledby": "description"}).find("div", class_="section-content").text


def get_accessibility_concerns(soup: BeautifulSoup) -> str:
    return (
        soup.find("section", attrs={"aria-labelledby": "accessibility_concerns"})
        .find("div", class_="section-content")
        .text
    )


def get_main_description(article: Tag) -> str:

    for child in article.children:
        if child.name == "section":
            return None
        if child.name == "div" and "section-content" in child.attrs.get("class"):
            div = child
            code_section = div.find("div", class_="code-example")
            if code_section:
                code_section.replace_with("")
            return div.text

    return None


section_scrapers = {
    "syntax": get_syntax_section,
    "formal_definition": get_formal_definition,
    "see_also": get_see_also,
    "constituent_properties": get_constituent_properties,
    "try_it": get_try_it,
    "description": get_description,
    "accessibility_concerns": get_accessibility_concerns,
}


def get_css_property_info_from_mdn_docs(css_property_name: str) -> dict[str, str] | None:
    url = f"https://developer.mozilla.org/en-US/docs/Web/CSS/{css_property_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.find(name="article", class_="main-page-content")
    if article.find(name="div", class_="experimental"):
        print(f"Skipping {css_property_name} because it is an EXPERIMENTAL property")
        return None
    if article.find(name="div", class_="deprecated"):
        print(f"Skipping {css_property_name} because it is a DEPRECATED property")
        return None

    main_description = get_main_description(article)
    if main_description is None:
        raise RuntimeError(f"{css_property_name} has no description")

    css_property_info = {
        "name": css_property_name,
        "url": url,
        "main_description": main_description,
    }

    for h2 in article.find_all(name="h2"):
        section_id = h2.text.lower().replace(" ", "_")
        scraper = section_scrapers.get(section_id)
        if scraper is None:
            continue
        if section_id == "try_it":
            css_property_info["main_description"] += scraper(soup)
        else:
            try:
                css_property_info[section_id] = scraper(soup)
            except Exception as e:
                raise e
                return None

    return css_property_info


def scrape_css_properties_info_from_mdn(output_file: str) -> None:

    with open("data/css-properties-names-list.txt", "r") as fp:
        css_property_names = [line.strip() for line in fp.readlines() if line.strip()]

    specs = []
    for css_property_name in tqdm(css_property_names):
        css_property_info = get_css_property_info_from_mdn_docs(css_property_name)
        if css_property_info:
            specs.append(css_property_info)

    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    with open(output_file, "w") as fp:
        json.dump(specs, fp, indent=4)

    print("[green bold]COMPLETE![/green bold]")
    print(f"\nScraped CSS properties info from MDN and saved it to {output_file}")


def cli():

    parser = argparse.ArgumentParser(
        description="Scrape CSS properties info from MDN and save it to a JSON file",
    )
    parser.add_argument(
        "--output-file",
        dest="output_file",
        default=DEFAULT_MDN_DOCS_JSON_FILENAME,
        type=str,
        help="Name of the output file",
    )
    args = parser.parse_args()
    scrape_css_properties_info_from_mdn(args.output_file)


if __name__ == "__main__":
    cli()
