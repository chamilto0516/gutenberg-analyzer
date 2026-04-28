# Gutenberg Word Frequency Analyzer - Project Context

## Project Overview
A Python CLI tool that searches for Project Gutenberg books via the Gutendex API, downloads the raw text, and generates a word frequency histogram for words 5 letters or longer.

## Tech Stack
- **Language:** Python 3.x (Standard Library only)
- **APIs:** 
  - [Gutendex](https://gutendex.com/) (Search/Discovery)
  - [Project Gutenberg Cache](https://www.gutenberg.org/cache/epub/) (Text Download)
- **Version Control:** Git/GitHub (`chamilto0516/gutenberg-analyzer`)

## Standards & Conventions
- **No External Dependencies:** Avoid `requests`, `pandas`, or `BeautifulSoup`. Use `urllib` and `re`.
- **Typing:** Use Python type hints (`typing` module) for all functions.
- **Constants:** Use uppercase constants for configuration (URL templates, limits, etc.).
- **Regex:** When using f-strings for regex quantifiers, use triple curly braces (e.g., `{{{MIN_LENGTH},}}`) to correctly escape the f-string interpolation.

## Current State
- [x] Search with Gutendex API.
- [x] Interactive selection for ambiguous titles.
- [x] Unique word count display.
- [x] Histogram generation with scaling.
- [x] VS Code Debug configurations (`launch.json`).

## Future Roadmap
- [ ] Add support for filtering out specific stop words.
- [ ] Add option to export data to CSV.
- [ ] Implement local caching of downloaded texts to avoid repeated network hits.
- [ ] Implement a log file that persists across multiple runs to track search history and analysis stats.
