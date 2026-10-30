# 🎵 Spotify Artist Data Extraction – Complete Guide

## 📊 Update (2025-10-08)

The script can now extract and save the following complete artist statistics to an Excel file:

### ✅ Automatically extracted data (via the API)

1. **Artist Name**
2. **Followers Count** - total number of Spotify followers
3. **Popularity Score** - rating from 0 to 100
4. **Genres** - all music styles
5. **Spotify URL** - link to the artist page
6. **Extraction Date** - recorded automatically

### ⭐ Manually added data

7. **Monthly Listeners** - must be looked up on the Spotify web page and entered manually

---

## 🚀 Three ways to use it

### Method 1: Quick interactive tool (easiest) ✨

```bash
python quick_add_listeners.py
```

**Advantages**:
- Interactive prompts, no need to remember complex commands
- Provides a Spotify search link
- Guided input of the monthly listeners count

**Workflow**:
1. Run the script
2. Enter the artist name
3. Visit the Spotify link provided
4. Enter the monthly listeners count you see
5. Choose whether you want the full analysis
6. All files are generated automatically

---

### Method 2: Command line (full control)

#### Basic usage

```bash
python code\spotify_artist_stats_and_visul_fetch.py "Artist Name" --monthly-listeners NUMBER
```

#### Full examples

```bash
# Venna - all features
python code\spotify_artist_stats_and_visul_fetch.py "Venna" \
    --monthly-listeners 500000 \
    --all-songs \
    --charts \
    --add-date

# Tom Misch - basic stats and charts only
python code\spotify_artist_stats_and_visul_fetch.py "Tom Misch" \
    --monthly-listeners 5200000 \
    --charts \
    --add-date

# Jay Chou - full analysis
python code\spotify_artist_stats_and_visul_fetch.py "Jay Chou" \
    --monthly-listeners 10000000 \
    --all-songs \
    --charts \
    --add-date
```

---

### Method 3: Without specifying monthly listeners

```bash
# If you do not have the monthly listeners data yet, you can omit it
python code\spotify_artist_stats_and_visul_fetch.py "Artist Name" --charts --add-date

# The Excel file will show "N/A"
```

---

## 📁 Output file structure

After running, the following files are created in the `result/Artist Name/` folder:

```
result/
└── Venna/
    ├── venna_artist_stats_20251008.xlsx    ⭐ Artist statistics (incl. monthly listeners)
    ├── venna_20251008.json                  Full JSON data
    ├── venna_20251008_popularity.png        Popularity chart (--charts)
    ├── venna_20251008_top_tracks.xlsx       Top tracks list (--charts)
    ├── venna_all_songs_20251008.xlsx        All songs list (--all-songs)
    └── venna_all_songs_20251008.json        All songs JSON (--all-songs)
```

---

## 📊 Excel statistics file details

### File name
- Format: `artistname_artist_stats_YYYYMMDD.xlsx`
- Example: `venna_artist_stats_20251008.xlsx`

### Columns

| Column | Data source | Example value |
|--------|-------------|---------------|
| Extraction Date | Generated automatically | 2025-10-08 |
| Artist Name | Spotify API | Venna |
| Monthly Listeners | Manual input | 500,000 |
| Followers | Spotify API | 78,294 |
| Popularity Score | Spotify API | 58 |
| Genres | Spotify API | jazz rap, uk r&b |
| Spotify URL | Spotify API | https://open.spotify.com/artist/... |

---

## 🔍 How to get the monthly listeners count

### Steps:

1. **Open the Spotify web player**
   ```
   https://open.spotify.com
   ```

2. **Search for the artist**
   - Type the artist name in the search box
   - Click the artist to open the artist page

3. **Look up the data**
   - Below the artist photo, next to the name, you will see:
     ```
     500,000 monthly listeners
     ```

4. **Note the number**
   - Copy the number (remove the commas)
   - 500,000 → enter `500000`

### Quick link:

```
https://open.spotify.com/search/ARTIST_NAME
```

---

## ⚙️ All command parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `Artist Name` | Required | The artist to analyze | `"Venna"` |
| `--monthly-listeners` | Optional | Manually specify the monthly listeners count | `--monthly-listeners 500000` |
| `--charts` | Optional | Generate visualization charts (PNG + Excel) | `--charts` |
| `--all-songs` | Optional | Fetch all songs (not just the top 10) | `--all-songs` |
| `--add-date` | Optional | Add the date to file names (recommended) | `--add-date` |
| `--from-date` | Optional | Only fetch songs after the given date | `--from-date 2020` |
| `--output-name` | Optional | Custom output file name | `--output-name my_analysis` |
| `--country` | Optional | Country market code | `--country US` |

---

## 💡 Best practices

### Recommended configuration:

```bash
python code\spotify_artist_stats_and_visul_fetch.py "Artist Name" \
    --monthly-listeners NUMBER_SEEN_ON_SPOTIFY \
    --all-songs \
    --charts \
    --add-date
```

This gives you:
- ✅ Complete artist statistics (including monthly listeners)
- ✅ List of all songs
- ✅ Visualization charts
- ✅ Date-stamped file names (easy to track)

### Regular updates:

```bash
# Re-run weekly/monthly to track changes
python code\spotify_artist_stats_and_visul_fetch.py "Venna" \
    --monthly-listeners LATEST_NUMBER \
    --charts \
    --add-date
```

Because `--add-date` is used, each run generates new files and never overwrites old data.

---

## 📝 Real-world use cases

### Case 1: Analyzing the new artist Venna

```bash
# 1. Visit Spotify and look up Venna
# Link: https://open.spotify.com/artist/7qKJMpPZfyGHHwPgsjgFCP

# 2. You see: 500,000 monthly listeners

# 3. Run the analysis
python code\spotify_artist_stats_and_visul_fetch.py "Venna" \
    --monthly-listeners 500000 \
    --all-songs \
    --charts \
    --add-date

# 4. View the result
# result/Venna/venna_artist_stats_20251008.xlsx
```

**Output data**:
- Monthly Listeners: 500,000
- Followers: 78,294
- Popularity: 58/100
- Genres: jazz rap, uk r&b

---

### Case 2: Tracking changes for Tom Misch

```bash
# First run (2025-10-08)
python code\spotify_artist_stats_and_visul_fetch.py "Tom Misch" \
    --monthly-listeners 5200000 \
    --charts \
    --add-date

# One month later (2025-11-08)
python code\spotify_artist_stats_and_visul_fetch.py "Tom Misch" \
    --monthly-listeners 5500000 \
    --charts \
    --add-date

# Result: the two files can be compared
# - tom_misch_artist_stats_20251008.xlsx
# - tom_misch_artist_stats_20251108.xlsx
```

---

## 🆘 FAQ

### Q1: Why can't monthly listeners be fetched automatically?
**A**: The official Spotify API does not provide this data. It is a statistic exclusive to the Spotify web interface and can only be looked up manually.

### Q2: What happens if I do not enter the monthly listeners?
**A**: The "Monthly Listeners" column in the Excel file shows "N/A"; all other data is displayed normally.

### Q3: Should the monthly listeners number include commas?
**A**: No. Enter a plain number, e.g. `500000` instead of `500,000`.

### Q4: How often is the data updated?
**A**: 
- **Followers, popularity**: real-time data; weekly updates are recommended
- **Monthly listeners**: changes daily; record it regularly

### Q5: How do I analyze multiple artists in bulk?
**A**: You can use a Windows batch script:

```batch
@echo off
python code\spotify_artist_stats_and_visul_fetch.py "Venna" --monthly-listeners 500000 --charts --add-date
python code\spotify_artist_stats_and_visul_fetch.py "Tom Misch" --monthly-listeners 5200000 --charts --add-date
python code\spotify_artist_stats_and_visul_fetch.py "Jay Chou" --monthly-listeners 10000000 --charts --add-date
```

---

## 📚 Related documents

- `artist_statistics_feature.md` - Introduction to the basic features
- `how_to_add_monthly_listeners.md` - Detailed monthly listeners guide
- `code/spotify_artist_stats_and_visul_fetch.py` - Main program
- `quick_add_listeners.py` - Quick interactive tool

---

## 🔧 Support

### Dependencies:

```bash
pip install requests python-dotenv pandas openpyxl matplotlib beautifulsoup4
```

### Environment setup:

Make sure the `.env` file contains your Spotify API credentials:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

---

## ✨ Summary

You can now:

1. ✅ Automatically extract an artist's followers, popularity and genres
2. ✅ Manually add monthly listeners data
3. ✅ Save all data to an Excel file that includes the extraction date
4. ✅ Generate visualization charts
5. ✅ Fetch the artist's complete song list
6. ✅ Track data changes regularly

**Get started**:

```bash
# The easiest way
python quick_add_listeners.py

# Or the full command
python code\spotify_artist_stats_and_visul_fetch.py "Artist Name" \
    --monthly-listeners NUMBER \
    --all-songs \
    --charts \
    --add-date
```

Enjoy! 🎵
