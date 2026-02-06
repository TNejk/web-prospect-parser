# Web Prospect Parser

A Python 3+ console tool to scrape current flyers (`Prospekte`) from [prospektmaschine.de/hypermarkte/](https://www.prospektmaschine.de/hypermarkte/) for all store chains in the Hypermärkte category. The output is saved as a JSON file with structured, consistent data.

---

## Features

- Scrapes all store chains in the Hypermärkte category (customizable).
- Validates flyer dates and stores them as objects.
- Outputs JSON with clean, standardized fields:
  - `title` – flyer title
  - `thumbnail` – flyer image URL
  - `shop_name` – name of the store
  - `valid_from` – start date of flyer (`YYYY-MM-DD`)
  - `valid_to` – end date of flyer (`YYYY-MM-DD` or `null` for long-term release)
  - `parsed_time` – timestamp when data was parsed (`YYYY-MM-DD HH:MM:SS`)
- Command-line interface for easy usage.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/TNejk/web-prospect-parser.git
cd web-prospect-parser
```

2. Install the package

```bash
pip install .
```

## Usage

Run the parser with default settings:
```bash
proser
```

This will scrape flyers from https://www.prospektmaschine.de/hypermarkte/ and save the output to `prospects.json` in the current directory.

Currently, you can optionally provide a category as an argument:
```bash
# example
proser /kleidung-schuhe-sport/
```
