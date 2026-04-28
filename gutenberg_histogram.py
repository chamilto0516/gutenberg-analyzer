#!/usr/bin/env python3
import urllib.request
import urllib.parse
import re
import json
from collections import Counter
import sys

def get_gutenberg_id(title):
    """Searches for a book by title using Gutendex API and returns the first Gutenberg ID found."""
    print(f"Searching for: {title}...")
    encoded_title = urllib.parse.quote(title)
    url = f"https://gutendex.com/books/?search={encoded_title}"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data['results']:
                # Return the ID of the first result
                return data['results'][0]['id']
            else:
                return None
    except Exception as e:
        print(f"Error during search: {e}")
        return None

def download_book_text(book_id):
    """Downloads the raw UTF-8 text for a given Gutenberg ID."""
    print(f"Downloading book ID {book_id}...")
    # Using the cache URL which is generally more reliable for direct text access
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading text: {e}")
        # Try fallback if cache URL fails (sometimes ID-0.txt is used)
        fallback_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
        print(f"Retrying with fallback: {fallback_url}")
        req = urllib.request.Request(fallback_url, headers=headers)
        try:
             with urllib.request.urlopen(req) as response:
                return response.read().decode('utf-8')
        except:
            return None

def analyze_text(text):
    """Analyzes the text and returns a Counter of words of 5+ letters."""
    # Find all alphabetic words with length >= 5
    words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
    return Counter(words)

def print_histogram(word_counts):
    """Prints a histogram of the word counts."""
    if not word_counts:
        print("No words found to display.")
        return

    max_count = word_counts[0][1]
    max_label_len = max(len(word) for word, count in word_counts)
    max_count_len = len(str(max_count))
    
    # Scale histogram to fit roughly 50 characters for the longest bar
    terminal_width_scale = 50
    
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

    book_id = get_gutenberg_id(book_name)
    if not book_id:
        print(f"Could not find a book with the title '{book_name}' on Project Gutenberg.")
        return

    text = download_book_text(book_id)
    if not text:
        print(f"Failed to download the text for '{book_name}' (ID: {book_id}).")
        return

    print("Analyzing text...")
    word_counter = analyze_text(text)
    unique_count = len(word_counter)
    top_words = word_counter.most_common(20)
    
    print(f"\nTotal unique words (5+ letters): {unique_count}")
    print_histogram(top_words)

if __name__ == "__main__":
    main()
