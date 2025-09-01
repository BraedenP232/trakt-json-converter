# Trakt JSON Converter

A Python script to convert Trakt export files into the format required for Trakt import. Useful for transferring watch history, ratings, and watchlist data between Trakt accounts.

## What it does

Trakt's export format is different from their import format. This script bridges that gap by converting your exported JSON files into the proper structure for importing.

**Supported export files:**
- `history-*.json` - Watch history with episodes, movies, shows
- `watched-movies.json` - Movie watch history  
- `watched-shows.json` - Show watch history

**Features:**
- Automatically detects file type
- Preserves watch dates, ratings, and watchlist data
- Prioritizes the best available IDs (IMDB > TMDB > TVDB > Trakt)
- Generates descriptive output filenames

## Installation

1. Clone this repository:
```bash
git clone https://github.com/BraedenP232/trakt-json-converter.git
cd trakt-json-converter
```

2. Make sure you have Python 3.6+ installed (no additional dependencies required)

## Usage

### Basic usage
```bash
python trakt_converter.py input_file.json
```

### Examples
```bash
# Convert history file (auto-generates history_import.json)
python trakt_converter.py history-1.json

# Convert movies with custom output name
python trakt_converter.py watched-movies.json my_movies_import.json

# Convert shows (auto-generates shows_import.json)  
python trakt_converter.py watched-shows.json
```

### Command format
```bash
python trakt_converter.py <input_file.json> [optional_output_file.json]
```

## How to get your Trakt export

1. Go to [Trakt->Settings->Data](https://trakt.tv/settings/data)
2. Request your data export
3. Download the ZIP file containing your JSON files
4. Unzip the file in your favourite tool. (WinRAR <3)

## Import process

1. Run this script on your exported JSON files
2. Upload the generated `*_import.json` files to your target Trakt account
3. Go to the import section in Trakt settings
4. Upload your converted files, one at a time.

## Output format

The script converts your exports into Trakt's import format:
```json
[
  {
    "imdb_id": "tt0068646",
    "type": "movie", 
    "watched_at": "2024-10-25T20:00:00Z",
    "rating": 8
  }
]
```

## Troubleshooting

**"No valid items found"** - The input file may be corrupted or in an unexpected format

**"File not found"** - Check that the file path is correct and the file exists

**"Invalid JSON"** - The input file is not valid JSON (may be corrupted)

## License

MIT License - see LICENSE file for details.
