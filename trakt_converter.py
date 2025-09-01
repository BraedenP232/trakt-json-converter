#!/usr/bin/env python3
"""
Trakt Export to Import Converter

Converts Trakt export files (history, watched-movies, watched-shows) 
to the format required for Trakt import.

Usage:
    python trakt_converter.py input_file.json [output_file.json]
    
Examples:
    python trakt_converter.py history-1.json
    python trakt_converter.py watched-movies.json movies_import.json
    python trakt_converter.py watched-shows.json
"""

import json
import sys
import os
from pathlib import Path


def extract_id(ids):
    """
    Pick the best ID available in order of preference.
    Priority: imdb > tmdb > tvdb > trakt
    """
    if ids.get("imdb"):
        return "imdb_id", ids["imdb"]
    elif ids.get("tmdb"):
        return "tmdb_id", ids["tmdb"]
    elif ids.get("tvdb"):
        return "tvdb_id", ids["tvdb"]
    elif ids.get("trakt"):
        return "trakt_id", ids["trakt"]
    return None, None


def convert_export_to_import(data):
    """
    Convert Trakt export data to import format.
    Handles multiple export formats: history, watched-movies, watched-shows.
    """
    result = []
    skipped_count = 0

    for item in data:
        id_key, id_value, item_type = None, None, None
        watched_at = None

        # --- History-style exports (history-1.json, etc.) ---
        if "type" in item:  
            item_type = item.get("type")
            
            if item.get("episode") and item["episode"].get("ids"):
                id_key, id_value = extract_id(item["episode"]["ids"])
            elif item.get("movie") and item["movie"].get("ids"):
                id_key, id_value = extract_id(item["movie"]["ids"])
            elif item.get("show") and item["show"].get("ids"):
                id_key, id_value = extract_id(item["show"]["ids"])
            elif item.get("season") and item["season"].get("ids"):
                id_key, id_value = extract_id(item["season"]["ids"])

            watched_at = item.get("watched_at")

        # --- Watched-movies.json style ---
        elif "movie" in item and item["movie"].get("ids"):
            id_key, id_value = extract_id(item["movie"]["ids"])
            item_type = "movie"
            watched_at = item.get("last_watched_at")

        # --- Watched-shows.json style ---
        elif "show" in item and item["show"].get("ids"):
            id_key, id_value = extract_id(item["show"]["ids"])
            item_type = "show"
            watched_at = item.get("last_watched_at")

        # Skip items without valid IDs
        if not id_key or not id_value:
            skipped_count += 1
            continue

        # Build the import entry
        entry = {
            id_key: id_value,
            "type": item_type,
        }

        # Add timestamps if available
        if watched_at:
            entry["watched_at"] = watched_at

        if "watchlisted_at" in item:
            entry["watchlisted_at"] = item["watchlisted_at"]

        # Add ratings if available
        if "rating" in item and item["rating"]:
            entry["rating"] = item["rating"]
            if "rated_at" in item:
                entry["rated_at"] = item["rated_at"]

        result.append(entry)

    if skipped_count > 0:
        print(f"⚠️  Skipped {skipped_count} items (no valid IDs found)")

    return result


def detect_file_type(data):
    """Detect the type of Trakt export file based on structure."""
    if not data or len(data) == 0:
        return "unknown"
    
    first_item = data[0]
    
    if "action" in first_item or "type" in first_item:
        return "history"
    elif "movie" in first_item:
        return "watched-movies"
    elif "show" in first_item:
        return "watched-shows"
    else:
        return "unknown"


def generate_output_filename(input_file):
    """Generate appropriate output filename based on input."""
    input_path = Path(input_file)
    stem = input_path.stem
    
    # Map common input names to descriptive output names
    name_mapping = {
        "history-1": "history_import",
        "history-2": "history_import",
        "history-3": "history_import", 
        "watched-movies": "movies_import",
        "watched-shows": "shows_import"
    }
    
    output_name = name_mapping.get(stem, f"{stem}_import")
    return f"{output_name}.json"


def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        print("❌ Error: Please provide an input file")
        print("\nUsage:")
        print("  python trakt_converter.py input_file.json [output_file.json]")
        print("\nExamples:")
        print("  python trakt_converter.py history-1.json")
        print("  python trakt_converter.py watched-movies.json movies_import.json")
        sys.exit(1)

    input_file = sys.argv[1]
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found")
        sys.exit(1)

    # Determine output file
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        output_file = generate_output_filename(input_file)

    try:
        # Load input file
        print(f"📖 Loading {input_file}...")
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("❌ Error: Expected JSON array format")
            sys.exit(1)

        # Detect file type
        file_type = detect_file_type(data)
        print(f"📋 Detected file type: {file_type}")
        print(f"📊 Found {len(data)} items to process")

        # Convert data
        print("🔄 Converting to import format...")
        converted = convert_export_to_import(data)

        if not converted:
            print("❌ No valid items found to convert")
            sys.exit(1)

        # Save output file
        print(f"💾 Saving to {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(converted, f, indent=2)

        print(f"✅ Success! Converted {len(converted)} items")
        print(f"📁 Output saved as: {output_file}")
        print(f"🚀 Ready to import into Trakt!")

    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format in {input_file}")
        print(f"   {str(e)}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ Error: Could not read {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
