import requests
import os
import hashlib
from urllib.parse import urlparse
import uuid

# Folder where images will be saved
DEST_DIR = "Fetched_Images"

# Track already-downloaded images by hash
downloaded_hashes = set()

def get_file_hash(content):
    """Return an MD5 hash for the given file content."""
    return hashlib.md5(content).hexdigest()

def fetch_image(url):
    """Download a single image from a URL into Fetched_Images folder."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(DEST_DIR, exist_ok=True)

        # Fetch headers first (HEAD request for metadata)
        head_resp = requests.head(url, timeout=10)
        if head_resp.status_code != 200:
            print(f"✗ Skipping {url} (HEAD request failed: {head_resp.status_code})")
            return

        # Check HTTP headers
        content_type = head_resp.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"⚠️ Skipping {url} (Content-Type is {content_type})")
            return

        content_length = head_resp.headers.get("Content-Length")
        if content_length and int(content_length) > 5_000_000:  # 5 MB limit
            print(f"⚠️ Skipping {url} (file too large: {int(content_length)/1_000_000:.2f} MB)")
            return

        # Fetch the actual image
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Check for duplicates
        file_hash = get_file_hash(response.content)
        if file_hash in downloaded_hashes:
            print(f"⚠️ Duplicate detected, skipping {url}")
            return
        downloaded_hashes.add(file_hash)

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # If no filename, generate a unique one
        if not filename:
            filename = f"downloaded_{uuid.uuid4().hex}.jpg"

        filepath = os.path.join(DEST_DIR, filename)

        # Avoid overwriting existing files
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join(DEST_DIR, f"{base}_{counter}{ext}")
            counter += 1

        # Save the image
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {os.path.basename(filepath)}")
        print(f"✓ Image saved to {filepath}\n")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred with {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    print("Enter image URLs (one per line).")
    print("When you are done, just press ENTER on an empty line:\n")

    urls = []
    while True:
        url = input("URL: ").strip()
        if not url:
            break
        urls.append(url)

    if not urls:
        print("No URLs entered. Exiting.")
        return

    print(f"\nFetching {len(urls)} image(s)...\n")
    for url in urls:
        fetch_image(url)

    print("All done. Connection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
