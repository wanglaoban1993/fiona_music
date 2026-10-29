# Artist Statistics Feature Documentation

## 📊 New Features

The script now automatically extracts and saves the following artist statistics to an Excel file:

### Extracted Data

1. **Extraction Date** - the date the data was extracted
2. **Artist Name** - the artist's full name
3. **Followers** - total number of followers on Spotify
4. **Popularity Score** - Spotify popularity rating (0-100)
5. **Genres** - the artist's music styles
6. **Spotify URL** - link to the artist on Spotify

---

## 🚀 Usage

### Basic Usage

```bash
# Analyze an artist and save the statistics
python spotify_artist_stats_and_visul_fetch.py "Artist Name"

# Examples:
python spotify_artist_stats_and_visul_fetch.py "Tom Misch"
python spotify_artist_stats_and_visul_fetch.py "Jay Chou"
python spotify_artist_stats_and_visul_fetch.py "Frankfurt Helmet"
```

### Full Analysis (all songs and charts)

```bash
# Fetch all songs + generate charts + add date stamp
python spotify_artist_stats_and_visul_fetch.py "Tom Misch" --all-songs --charts --add-date
```

### Parameter Descriptions

| Parameter | Description |
|-----------|-------------|
| `--charts` | Generate popularity visualization charts (PNG files) |
| `--all-songs` | Fetch all of the artist's songs (not just the first 10) |
| `--add-date` | Add the date to file names (YYYYMMDD format) |
| `--from-date 2020` | Only fetch songs after 2020 (must be used with --all-songs) |
| `--output-name custom_name` | Custom output file name |

---

## 📁 Output Files

The script creates the following files in the `result/artist_name/` folder:

### Automatically Generated Files

1. **Artist Statistics**
   - File name format: `artistname_artist_stats_20251008.xlsx`
   - Contains followers, popularity, extraction date, etc.

2. **JSON Data**
   - File name format: `artistname_20251008.json`
   - Contains the complete API response data

### Optional Files (with parameters)

3. **All songs list** (when using `--all-songs`)
   - Excel: `artistname_all_songs_20251008.xlsx`
   - JSON: `artistname_all_songs_20251008.json`

4. **Visualization charts** (when using `--charts`)
   - Popularity chart: `artistname_20251008_popularity.png`
   - Top tracks Excel: `artistname_20251008_top_tracks.xlsx`

---

## 📝 Excel File Example

### Artist statistics table example:

| Extraction Date | Artist Name | Followers | Popularity Score | Genres | Spotify URL |
|-----------------|-------------|-----------|------------------|--------|-------------|
| 2025-10-08 | Tom Misch | 1,234,567 | 78 | Jazz, Soul, Electronic | https://... |

---

## 💡 Usage Examples

### Example 1: Quick analysis (statistics only)
```bash
python spotify_artist_stats_and_visul_fetch.py "Venna"
```
**Output**: 
- `result/Venna/venna_artist_stats_20251008.xlsx`
- `result/Venna/venna_20251008.json`

### Example 2: Full analysis (all features)
```bash
python spotify_artist_stats_and_visul_fetch.py "Tom Misch" --all-songs --charts --add-date
```
**Output**:
- `result/Tom_Misch/tom_misch_artist_stats_20251008.xlsx` ✅ New!
- `result/Tom_Misch/tom_misch_20251008.json`
- `result/Tom_Misch/tom_misch_all_songs_20251008.xlsx`
- `result/Tom_Misch/tom_misch_all_songs_20251008.json`
- `result/Tom_Misch/tom_misch_20251008_popularity.png`
- `result/Tom_Misch/tom_misch_20251008_top_tracks.xlsx`

### Example 3: Using the test script
```bash
python test/test_artist_stats.py "Jay Chou"
```

---

## ⚠️ Important Notes

### About Monthly Listeners

**Note**: Spotify's official API **does NOT provide** Monthly Listeners data.

This data is only visible on Spotify's web/app interface and cannot be accessed via the API. The script currently provides:

- ✅ **Followers Count** - available via the API
- ✅ **Popularity Score** - available via the API
- ❌ **Monthly Listeners** - not supported by the API

### Data Notes

- **Followers**: total number of users following the artist on Spotify
- **Popularity**: a 0-100 score calculated from play counts, recency of plays, etc.
- **Extraction Date**: automatically records the date the data was extracted, making it easy to track changes

---

## 🔧 Dependencies

Make sure the following Python packages are installed:

```bash
pip install requests python-dotenv pandas openpyxl matplotlib
```

---

## 📞 Support

For issues, please check:
- Spotify API credentials in the `.env` file
- Network connection
- Python dependencies are properly installed
