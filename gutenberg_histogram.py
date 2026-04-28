#!/usr/bin/env python3
import urllib.request
import urllib.parse
import re
import json
from collections import Counter
import sys
from typing import List, Dict, Optional, Union, Tuple, Any

# Constants
GUTENDEX_API_URL = "https://gutendex.com/books/"
GUTENBERG_CACHE_URL_TEMPLATE = "https://www.gutenberg.org/cache/epub/{}/pg{}.txt"
GUTENBERG_FALLBACK_URL_TEMPLATE = "https://www.gutenberg.org/files/{}/{}-0.txt"
USER_AGENT = 'Mozilla/5.0'
TERMINAL_WIDTH_SCALE = 50
MIN_WORD_LENGTH = 5
TOP_RESULTS_LIMIT = 10
TOP_WORDS_LIMIT = 20

def get_gutenberg_id(title: str) -> List[Dict[str, Union[int, str]]]:
    """Searches for a book by title using Gutendex API and returns a list of matching books."""
    print(f"Searching for: {title}...")
    encoded_title = urllib.parse.quote(title)
    url = f"{GUTENDEX_API_URL}?search={encoded_title}"
    
    headers = {'User-Agent': USER_AGENT}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('results', [])
            # Return list of dicts with id and title
            return [{'id': r['id'], 'title': r['title']} for r in results if 'id' in r and 'title' in r]
    except Exception as e:
        print(f"Error during search: {e}")
        return []

def download_book_text(book_id: int) -> Optional[str]:
    """Downloads the raw UTF-8 text for a given Gutenberg ID."""
    print(f"Downloading book ID {book_id}...")
    # Using the cache URL which is generally more reliable for direct text access
    url = GUTENBERG_CACHE_URL_TEMPLATE.format(book_id, book_id)
    
    headers = {'User-Agent': USER_AGENT}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading text: {e}")
        # Try fallback if cache URL fails (sometimes ID-0.txt is used)
        fallback_url = GUTENBERG_FALLBACK_URL_TEMPLATE.format(book_id, book_id)
        print(f"Retrying with fallback: {fallback_url}")
        req = urllib.request.Request(fallback_url, headers=headers)
        try:
             with urllib.request.urlopen(req) as response:
                return response.read().decode('utf-8')
        except:
            return None

def analyze_text(text: str) -> Counter:
    """Analyzes the text and returns a Counter of words of 5+ letters."""
    # Find all alphabetic words with length >= 5
    # Use triple curly braces to escape for f-string and provide the regex quantifier
    words = re.findall(rf'\b[a-zA-Z]{{{MIN_WORD_LENGTH},}}\b', text.lower())
    return Counter(words)

def print_histogram(word_counts: List[Tuple[str, int]]) -> None:
    """Prints a histogram of the word counts."""
    if not word_counts:
        print("No words found to display.")
        return

    max_count = word_counts[0][1]
    max_label_len = max(len(word) for word, count in word_counts)
    max_count_len = len(str(max_count))
    
    # Scale histogram to fit roughly 50 characters for the longest bar
    terminal_width_scale = TERMINAL_WIDTH_SCALE
    
    print("\nMost Common Words (5+ letters):\n")
    print(f"{'WORD'.ljust(max_label_len)} | {'COUNT'.ljust(max_count_len)} | HISTOGRAM")
    print("-" * (max_label_len + max_count_len + terminal_width_scale + 6))
    
    for word, count in word_counts:
        bar_len = int((count / max_count) * terminal_width_scale)
        bar = "*" * bar_len
        print(f"{word.ljust(max_label_len)} | {str(count).ljust(max_count_len)} | {bar}")

def main():
    if len(sys.argv) < 2:
        book_name = input("Enter the name of the book: ")
    else:
        book_name = " ".join(sys.argv[1:])

    if not book_name.strip():
        print("Invalid book name.")
        return

    matches = get_gutenberg_id(book_name)
    if not matches:
        print(f"Could not find any books matching '{book_name}' on Project Gutenberg.")
        return

    # If the first result is a very close match, just use it
    # Otherwise, show the top 10 and let them pick
    selected_book = None
    if len(matches) == 1 or matches[0]['title'].lower() == book_name.lower():
        selected_book = matches[0]
    else:
        print(f"\nMultiple results found for '{book_name}'. Please choose one:")
        top_10 = matches[:TOP_RESULTS_LIMIT]
        for i, book in enumerate(top_10, 1):
            print(f"{i}. {book['title']} (ID: {book['id']})")
        
        try:
            choice = input(f"\nSelect a number (1-{len(top_10)}) or press Enter for #1: ")
            if not choice.strip():
                selected_book = top_10[0]
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(top_10):
                    selected_book = top_10[idx]
                else:
                    print("Invalid selection. Using the first result.")
                    selected_book = top_10[0]
        except ValueError:
            print("Invalid input. Using the first result.")
            selected_book = top_10[0]

    book_id = selected_book['id']
    book_title = selected_book['title']
    print(f"\nSelected: {book_title}")

    text = download_book_text(book_id)
    if not text:
        print(f"Failed to download the text for '{book_title}' (ID: {book_id}).")
        return

    print("Analyzing text...")
    word_counter = analyze_text(text)
    unique_count = len(word_counter)
    top_words = word_counter.most_common(TOP_WORDS_LIMIT)
    
    print(f"\nTotal unique words (5+ letters): {unique_count}")
    print_histogram(top_words)

if __name__ == "__main__":
    main()
