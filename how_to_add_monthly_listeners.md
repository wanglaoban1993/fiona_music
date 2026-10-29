# 🎧 How to Get and Add Monthly Listeners Data

## 📊 Update notes

The script now supports adding **Monthly Listeners** data to the Excel statistics file!

### ✅ New feature

The file `artistname_artist_stats_YYYYMMDD.xlsx` now contains:

| Extraction Date | Artist Name | Monthly Listeners | Followers | Popularity Score | Genres | Spotify URL |
|-----------------|-------------|-------------------|-----------|------------------|--------|-------------|
| 2025-10-08 | Venna | 500,000 | 78,294 | 58 | jazz rap, uk r&b | https://... |

---

## 🔍 How to get the monthly listeners data

### ⚠️ Important

**The official Spotify API does not provide monthly listeners data.** This data can only be looked up manually on the Spotify web page or mobile app.

### Steps:

1. **Open the Spotify web player**
   - Visit: https://open.spotify.com
   - Search for the artist name

2. **Open the artist page**
   - At the top of the artist page, below the artist name, you will see something like:
     ```
     500,000 monthly listeners
     ```

3. **Note the number**
   - Copy the number (remove the commas)
   - Example: 500,000 → enter 500000

---

## 💻 Usage

### Method 1: Specify the monthly listeners manually (recommended)

```bash
# Basic usage
python spotify_artist_stats_and_visul_fetch.py "Artist Name" --monthly-listeners NUMBER

# Full example
python spotify_artist_stats_and_visul_fetch.py "Venna" --monthly-listeners 500000 --charts --add-date
```

### Method 2: Do not specify (shown as N/A)

```bash
# If omitted, the Excel file shows "N/A"
python spotify_artist_stats_and_visul_fetch.py "Venna" --charts --add-date
```

---

## 📝 Real-world examples

### Example 1: Venna

1. **Check on Spotify**: open https://open.spotify.com/artist/7qKJMpPZfyGHHwPgsjgFCP
2. **You see**: 500,000 monthly listeners
3. **Run the command**:
   ```bash
   python test\spotify_artist_stats_and_visul_fetch.py "Venna" --monthly-listeners 500000 --charts --add-date
   ```
4. **View the result**: `result/Venna/venna_artist_stats_20251008.xlsx`

### Example 2: Tom Misch

1. **Check on Spotify**: https://open.spotify.com/artist/1uiEZYehlNivdK3iQyAbye
2. **Suppose you see**: 5,200,000 monthly listeners
3. **Run the command**:
   ```bash
   python test\spotify_artist_stats_and_visul_fetch.py "Tom Misch" --monthly-listeners 5200000 --all-songs --charts --add-date
   ```

### Example 3: Jay Chou

1. **Check the artist page on Spotify**
2. **Note the monthly listeners count** (e.g. 10,000,000)
3. **Run the command**:
   ```bash
   python test\spotify_artist_stats_and_visul_fetch.py "Jay Chou" --monthly-listeners 10000000 --charts --add-date
   ```

---

## 🎯 Complete workflow

### Recommended steps:

```bash
# 1. Look up the artist on the Spotify web player
# Visit: https://open.spotify.com/search/ARTIST_NAME

# 2. Note the monthly listeners number

# 3. Run the full analysis command
python test\spotify_artist_stats_and_visul_fetch.py "Artist Name" \
    --monthly-listeners NUMBER \
    --all-songs \
    --charts \
    --add-date

# Example (Windows PowerShell):
python test\spotify_artist_stats_and_visul_fetch.py "Venna" --monthly-listeners 500000 --all-songs --charts --add-date
```

---

## 📁 Output files

After running, the following files are generated:

```
result/
└── Venna/
    ├── venna_artist_stats_20251008.xlsx    ← Contains the monthly listeners data!
    ├── venna_20251008.json
    ├── venna_all_songs_20251008.xlsx
    ├── venna_all_songs_20251008.json
    ├── venna_20251008_popularity.png
    └── venna_20251008_top_tracks.xlsx
```

---

## 📊 Excel file content example

**venna_artist_stats_20251008.xlsx** contains:

| Column | Example value | Description |
|--------|---------------|-------------|
| Extraction Date | 2025-10-08 | Date the data was extracted |
| Artist Name | Venna | Full artist name |
| Monthly Listeners | 500,000 | Obtained manually from the Spotify web page |
| Followers | 78,294 | Fetched automatically via the API |
| Popularity Score | 58 | Fetched automatically via the API (0-100) |
| Genres | jazz rap, uk r&b | Fetched automatically via the API |
| Spotify URL | https://open.spotify.com/... | Artist link |

---

## ⚙️ Command parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--monthly-listeners NUMBER` | Manually specify the monthly listeners count | `--monthly-listeners 500000` |
| `--charts` | Generate visualization charts | `--charts` |
| `--all-songs` | Fetch all songs (not just the top 10) | `--all-songs` |
| `--add-date` | Add the date to file names | `--add-date` |
| `--from-date 2020` | Only fetch songs after 2020 | `--from-date 2020` |
| `--output-name custom` | Custom output file name | `--output-name venna_analysis` |

---

## 🆘 FAQ

### Q1: Why can't the monthly listeners count be fetched automatically?
**A**: The official Spotify API does not provide this data. It can only be looked up manually on the web page or in the app.

### Q2: What if I do not know the monthly listeners count?
**A**: Omit the `--monthly-listeners` parameter; the Excel file will show "N/A".

### Q3: Should the number include commas?
**A**: No. Enter a plain number, e.g. 500000 (not 500,000).

### Q4: Does the monthly listeners count change?
**A**: Yes! It is real-time data and changes every day. Use the `--add-date` parameter to record the extraction date.

---

## 💡 Tips

1. **Use the `--add-date` parameter**: lets you track changes across dates
2. **Update regularly**: monthly listeners is dynamic data, so re-fetch it periodically
3. **Keep backups**: the Excel files contain the extraction date, making it easy to compare historical data

---

## 📞 Support

If you run into problems, check:
- Whether the Spotify web page is reachable
- Whether the monthly listeners number is correct (plain number, no commas)
- Whether the Python environment is configured correctly
