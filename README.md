# fiona_music

A Python toolkit for collecting and analysing Spotify artist data (followers, popularity, genres, albums, tracks) via the Spotify Web API, with Excel/JSON export and popularity charts.

> The repository also contains an unrelated experiment: a causal-inference / SHAP demo on the Boston housing data (`boston_causal_mlp.py`, `test_anything.ipynb`).

## Features

- Artist search and statistics: followers, popularity score, genres, Spotify URL
- Top tracks, albums and the **full song catalogue** (deduplicated across albums)
- Optional date filter for songs (`--from-date`)
- Export to JSON and Excel, optional popularity charts (PNG)
- Monthly listeners via manual input (Spotify's public API does not provide it; missing values are written as `N/A`)

## Setup

```bash
pip install -r requirements.txt
```

Create Spotify API credentials at <https://developer.spotify.com/dashboard/>, then copy `.env.example` to `code/.env` and fill it in:

```powershell
Copy-Item .env.example code\.env
```

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

`.env` is git-ignored. Never commit real credentials.

## Usage

Run from the repository root:

```bash
# Basic statistics
python code/spotify_artist_stats_and_visul_fetch.py "Tom Misch"

# Full analysis: all songs, charts, date-stamped file names, manual monthly listeners
python code/spotify_artist_stats_and_visul_fetch.py "Tom Misch" --all-songs --charts --add-date --monthly-listeners 5200000

# Interactive helper
python quick_add_listeners.py
```

| Option | Description |
|--------|-------------|
| `--all-songs` | Fetch every song, not just the top 10 |
| `--from-date 2020` | Only songs released from this date (needs `--all-songs`) |
| `--charts` | Create popularity chart (PNG) and top-tracks Excel |
| `--add-date` | Append `YYYYMMDD` to output file names |
| `--monthly-listeners N` | Add monthly listeners (looked up manually on Spotify) |
| `--output-name NAME` | Custom output file name |
| `--country US` | Market code used for top tracks |

Output is written to `result/<artist>/`, for example `venna_artist_stats_20251008.xlsx`, `venna_20251008.json`, `venna_all_songs_20251008.xlsx` and `venna_20251008_popularity.png`.

## Project layout

```
code/                          Spotify analyser (main script, search helper, test script)
quick_add_listeners.py         Interactive CLI wrapper
result/                        Example output per artist
boston_causal_mlp.py           Deep Double ML + SHAP demo (separate experiment)
*.md                           Detailed feature documentation
```

## Documentation

- [artist_statistics_feature.md](artist_statistics_feature.md) – statistics feature overview
- [how_to_add_monthly_listeners.md](how_to_add_monthly_listeners.md) – monthly listeners guide
- [README_monthly_listeners.md](README_monthly_listeners.md) – complete usage guide

## Known limitations

- Monthly listeners are not available through the official API and must be entered manually.
- The `related-artists` endpoint is restricted by Spotify for newer apps and typically returns nothing.
- Results are single-day snapshots; popularity and follower counts change over time.
