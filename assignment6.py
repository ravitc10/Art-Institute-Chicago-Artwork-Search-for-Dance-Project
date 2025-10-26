# import libraries: requests, json
import requests
import json

# Define the base URL for the Art Institute of Chicago API search endpoint
base_url = "https://api.artic.edu/api/v1/artworks/search"

# Function to get artwork information based on a search term. Define parameters for the search term and amount of responses. 
def get_artwork_info(search_term, limit=10):
    params = {"q": search_term, "limit": limit}
    try:
        resp = requests.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        if "resp" in locals():
            print("request failed:", resp.status_code)
            print(resp.text)
        else:
            print("request failed:", e)
        return None

# Try to parse the response as JSON, otherwise return raw text
    try:
        return resp.json()
    except ValueError:
        print("response is not JSON; returning raw text")
        return resp.text

# Function that makes responses easier to understand for the user
def pretty_print_artworks(info):
    if not info:
        print("No results")
        return

    # Search responses include a 'data' list
    data = info.get("data") if isinstance(info, dict) else None
    if not data:
        # fallback: raw pretty JSON
        print(json.dumps(info, indent=2))
        return

# Find and print meta data (dictionary of data) about the search results
    meta = info.get("meta", {})
    found = meta.get("found", len(data))
    print(f"Found ~{found} result(s). Showing {len(data)}:\n")

# Iterate through each artwork item and print relevant details, like title, artist, description, and ID
    for i, item in enumerate(data, start=1):
        title = item.get("title") or item.get("display_title") or "<no title>"
        artist = (item.get("artist_display") or "").strip()

        # Try common places for alt/text description
        text = item.get("alt_text")
        if not text:
            thumb = item.get("thumbnail") or {}
            text = thumb.get("alt_text")
        if isinstance(text, str):
            text = text.strip()
        else:
            text = None
# Get the artwork ID
        art_id = item.get("id")
        print(f"{i}. {title}")
        if artist:
            print(f"   Artist: {artist}")
        if text:
            print(f"   Description: {text}")
        if art_id is not None:
            print(f"   ID: {art_id}")
        print("-" * 90)

# Interactive prompt for user input
def interactive_search():
    """Prompt the user for a search term, fetch results, and pretty-print them."""
    term = input("Enter search term (or leave empty to cancel): ").strip()
    if not term:
        print("No search term provided; exiting.")
        return
    info = get_artwork_info(term, limit=10)
    pretty_print_artworks(info)

if __name__ == "__main__":
    # Run interactive function
    interactive_search()

