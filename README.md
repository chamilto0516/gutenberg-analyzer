# Gutenberg Word Frequency Analyzer

A Python 3 utility that searches for books on Project Gutenberg, downloads their full text, and generates a terminal-based histogram of the most frequent words (5 letters or longer).

## Features

- **Search by Title:** Automatically finds the correct Project Gutenberg ID using the Gutendex API.
- **Auto-Download:** Fetches the raw UTF-8 text directly from Gutenberg's servers.
- **Frequency Analysis:** Filters for words with 5 or more letters to provide more meaningful insights (ignoring common words like "the", "and", "a").
- **Visual Histogram:** Prints a scaled ASCII histogram in the terminal.
- **Zero Dependencies:** Uses only Python standard libraries—no `pip install` required.

## Installation

Ensure you have Python 3.x installed on your machine.

```bash
git clone https://github.com/chamilto0516/gutenberg-analyzer.git
cd gutenberg-analyzer
```

## Usage

You can run the script by passing the book title as an argument:

```bash
python3 gutenberg_histogram.py "Pride and Prejudice"
```

Or run it without arguments to be prompted for a title:

```bash
python3 gutenberg_histogram.py
```

## Sample Output

```text
Most Common Words (5+ letters):

WORD      | COUNT | HISTOGRAM
--------------------------------------------------------------------
elizabeth | 645 | **************************************************
which     | 574 | ********************************************
could     | 531 | *****************************************
would     | 482 | *************************************
their     | 452 | ***********************************
darcy     | 430 | *********************************
there     | 369 | ****************************
```

## License

This project is open-source and available under the MIT License.
