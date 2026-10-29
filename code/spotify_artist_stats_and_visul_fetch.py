import os
import json
import argparse
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, List
import re

class SpotifyArtistAnalyzer:
    """A comprehensive Spotify artist data analyzer"""
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        """Initialize with Spotify credentials"""
        load_dotenv()
        
        self.client_id = client_id or os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("SPOTIFY_CLIENT_SECRET")
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials required. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET")
        
        self.token = None
        self.base_url = "https://api.spotify.com/v1"
        self.token_url = "https://accounts.spotify.com/api/token"
        
        # Current analysis data
        self.current_artist = None
        self.current_data = None
    
    def _get_token(self) -> str:
        """Get or refresh Spotify access token"""
        if self.token:
            return self.token
            
        resp = requests.post(
            self.token_url,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
            timeout=20,
        )
        resp.raise_for_status()
        self.token = resp.json()["access_token"]
        return self.token
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make authenticated request to Spotify API"""
        headers = {"Authorization": f"Bearer {self._get_token()}"}
        url = f"{self.base_url}/{endpoint}"
        
        response = requests.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        return response.json()
    
    def _get_monthly_listeners(self, artist_id: str) -> Optional[int]:
        """
        Attempt to get monthly listeners by scraping Spotify web page
        Note: This is not available via official API
        """
        try:
            # Try using Spotify embed API endpoint (sometimes has this data)
            embed_url = f"https://open.spotify.com/embed/artist/{artist_id}"
            web_url = f"https://open.spotify.com/artist/{artist_id}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            # Try main page first
            response = requests.get(web_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Look for monthly listeners in the HTML
            # Spotify may use different formats
            patterns = [
                r'(\d[\d,\.]*)\s*monthly\s*listeners',
                r'monthly\s*listeners[^\d]*(\d[\d,\.]*)',
                r'(\d[\d,\.]*)\s*oyentes\s*mensuales',  # Spanish
                r'(\d[\d,\.]*)\s*auditeurs\s*mensuels',  # French
                r'(\d[\d,\.]*)\s*monatliche\s*Hörer',  # German
                r'"monthlyListeners"[:\s]*(\d+)',  # JSON format
                r'monthly_listeners["\s:]*(\d+)',  # Alternative JSON
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE)
                for match in matches:
                    try:
                        # Extract number and remove commas/dots (except decimal points)
                        listeners_str = match.replace(',', '').replace('.', '')
                        listeners = int(listeners_str)
                        # Sanity check: should be between 1 and 100 million
                        if 1 < listeners < 100000000:
                            print(f"✅ Monthly listeners found: {listeners:,}")
                            return listeners
                    except (ValueError, AttributeError):
                        continue
            
            # If not found, try to parse as BeautifulSoup
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for text containing "monthly listeners"
                for text in soup.stripped_strings:
                    if 'monthly' in text.lower() and 'listener' in text.lower():
                        # Extract numbers from this text
                        numbers = re.findall(r'\d[\d,\.]*', text)
                        for num_str in numbers:
                            try:
                                listeners = int(num_str.replace(',', '').replace('.', ''))
                                if 1 < listeners < 100000000:
                                    print(f"✅ Monthly listeners found (via BS4): {listeners:,}")
                                    return listeners
                            except ValueError:
                                continue
            except ImportError:
                pass  # BeautifulSoup not available
            
            print("⚠️  Could not extract monthly listeners from web page")
            print("   (This data is not available via Spotify API)")
            return None
            
        except Exception as e:
            print(f"⚠️  Could not fetch monthly listeners: {e}")
            return None
    
    def find_artist(self, name: str) -> Optional[Dict]:
        """Find artist by name"""
        
        params = {
            "q": name,  # Don't URL encode - requests does it automatically
            "type": "artist",
            "limit": 10  # Get more results to find exact match
        }
        
        data = self._make_request("search", params)
        items = data.get("artists", {}).get("items", [])
        
        if not items:
            return None
        
        # Try to find exact match first (case-insensitive)
        name_lower = name.lower()
        for artist in items:
            if artist["name"].lower() == name_lower:
                # Exact match found!
                print(f"✅ Exact match found: {artist['name']}")
                self.current_artist = {
                    "id": artist["id"],
                    "name": artist["name"],
                    "url": artist["external_urls"]["spotify"],
                    "followers": artist["followers"]["total"],
                    "popularity": artist["popularity"],
                    "genres": artist["genres"],
                    "images": artist["images"]
                }
                
                # Try to get monthly listeners from web scraping
                self.current_artist["monthly_listeners"] = self._get_monthly_listeners(artist["id"])
                
                return self.current_artist
        
        # No exact match, use first result but warn user
        artist = items[0]
        print(f"⚠️  No exact match for '{name}'")
        print(f"   Using closest match: '{artist['name']}'")
        print(f"   (Followers: {artist['followers']['total']:,}, Popularity: {artist['popularity']}/100)")
        
        self.current_artist = {
            "id": artist["id"],
            "name": artist["name"],
            "url": artist["external_urls"]["spotify"],
            "followers": artist["followers"]["total"],
            "popularity": artist["popularity"],
            "genres": artist["genres"],
            "images": artist["images"]
        }
        
        # Try to get monthly listeners from web scraping
        self.current_artist["monthly_listeners"] = self._get_monthly_listeners(artist["id"])
        
        return self.current_artist
    
    def get_top_tracks(self, artist_id: str = None, country: str = "US") -> List[Dict]:
        """Get artist's top tracks"""
        artist_id = artist_id or self.current_artist["id"]
        
        params = {"market": country}
        data = self._make_request(f"artists/{artist_id}/top-tracks", params)
        
        tracks = []
        for track in data.get("tracks", []):
            track_info = {
                "name": track["name"],
                "popularity": track["popularity"],
                "duration_ms": track["duration_ms"],
                "duration_min": round(track["duration_ms"] / 60000, 2),
                "explicit": track["explicit"],
                "preview_url": track["preview_url"],
                "spotify_url": track["external_urls"]["spotify"],
                "album": {
                    "name": track["album"]["name"],
                    "release_date": track["album"]["release_date"],
                    "total_tracks": track["album"]["total_tracks"]
                },
                "artists": [artist["name"] for artist in track["artists"]]
            }
            tracks.append(track_info)
        
        return tracks
    
    def get_albums(self, artist_id: str = None, limit: int = 50) -> List[Dict]:
        """Get artist's albums (increased limit to get more albums)"""
        artist_id = artist_id or self.current_artist["id"]
        
        params = {
            "include_groups": "album,single",
            "market": "US",
            "limit": limit
        }
        
        data = self._make_request(f"artists/{artist_id}/albums", params)
        
        albums = []
        for album in data.get("items", []):
            album_info = {
                "id": album["id"],
                "name": album["name"],
                "release_date": album["release_date"],
                "total_tracks": album["total_tracks"],
                "album_type": album["album_type"],
                "spotify_url": album["external_urls"]["spotify"]
            }
            albums.append(album_info)
        
        return albums
    
    def get_related_artists(self, artist_id: str = None, limit: int = 10) -> List[Dict]:
        """Get related artists"""
        artist_id = artist_id or self.current_artist["id"]
        
        try:
            data = self._make_request(f"artists/{artist_id}/related-artists")
            
            related = []
            for artist in data.get("artists", [])[:limit]:
                artist_info = {
                    "name": artist["name"],
                    "popularity": artist["popularity"],
                    "followers": artist["followers"]["total"],
                    "spotify_url": artist["external_urls"]["spotify"],
                    "genres": artist["genres"]
                }
                related.append(artist_info)
            
            return related
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Could not fetch related artists: {e}")
            return []
    
    def get_album_tracks(self, album_id: str) -> List[Dict]:
        """Get all tracks from a specific album"""
        try:
            data = self._make_request(f"albums/{album_id}/tracks")
            tracks = []
            
            for track in data.get("items", []):
                track_info = {
                    "id": track["id"],
                    "name": track["name"],
                    "track_number": track["track_number"],
                    "duration_ms": track["duration_ms"],
                    "explicit": track["explicit"],
                    "spotify_url": track["external_urls"]["spotify"]
                }
                tracks.append(track_info)
            
            return tracks
        except Exception as e:
            print(f"⚠️  Could not fetch album tracks: {e}")
            return []
    
    def get_all_songs(self, artist_id: str = None, from_date: str = None) -> List[Dict]:
        """
        Get ALL songs from an artist (from all albums)
        
        Args:
            artist_id: Spotify artist ID
            from_date: Filter songs from this date onwards (format: YYYY-MM-DD or YYYY)
        
        Returns:
            List of all tracks with popularity data
        """
        artist_id = artist_id or self.current_artist["id"]
        
        print("📀 Fetching all albums...")
        albums = self.get_albums(artist_id, limit=50)
        
        # Filter albums by date if specified
        if from_date:
            print(f"📅 Filtering albums from {from_date} onwards...")
            albums = [a for a in albums if a["release_date"] >= from_date]
        
        print(f"📀 Found {len(albums)} albums")
        
        all_songs = []
        seen_track_ids = set()
        
        for i, album in enumerate(albums, 1):
            print(f"   Processing album {i}/{len(albums)}: {album['name']}")
            
            # Get album tracks
            album_tracks = self.get_album_tracks(album["id"])
            
            # Get detailed track info with popularity
            for track in album_tracks:
                # Skip duplicates (songs appear in multiple albums)
                if track["id"] in seen_track_ids:
                    continue
                seen_track_ids.add(track["id"])
                
                try:
                    # Get full track info with popularity
                    track_data = self._make_request(f"tracks/{track['id']}")
                    
                    song_info = {
                        "name": track_data["name"],
                        "popularity": track_data["popularity"],
                        "album": album["name"],
                        "release_date": album["release_date"],
                        "album_type": album["album_type"],
                        "explicit": track_data["explicit"],
                        "spotify_url": track_data["external_urls"]["spotify"],
                        "artists": [a["name"] for a in track_data["artists"]]
                    }
                    all_songs.append(song_info)
                    
                except Exception as e:
                    print(f"⚠️  Could not fetch track {track['name']}: {e}")
                    continue
        
        print(f"✅ Found {len(all_songs)} unique songs")
        return all_songs
    
    def save_all_songs_to_excel(self, songs: List[Dict] = None, output_dir: str = "result", 
                                filename: str = None, include_date: bool = False) -> str:
        """Save all songs with popularity to Excel file"""
        import pandas as pd
        
        if songs is None:
            print("❌ No songs data provided")
            return None
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Prepare data for Excel
        df = pd.DataFrame(songs)
        
        # Sort by popularity (highest first)
        df = df.sort_values('popularity', ascending=False)
        
        # Generate filename
        if filename is None:
            artist_name = self.current_artist["name"]
            clean_name = artist_name.replace(' ', '_').lower()
            
            # Add date if requested
            if include_date:
                from datetime import datetime
                date_str = datetime.now().strftime("%Y%m%d")
                filename = f"{clean_name}_all_songs_{date_str}.xlsx"
            else:
                filename = f"{clean_name}_all_songs_popularity.xlsx"
        
        filepath = os.path.join(output_dir, filename)
        
        # Save to Excel
        df.to_excel(filepath, index=False)
        print(f"📊 Saved {len(songs)} songs to: {filepath}")
        
        return filepath
    
    def save_artist_stats_to_excel(self, output_dir: str = "result", 
                                   filename: str = None, include_date: bool = True) -> str:
        """
        Save artist statistics to Excel file including:
        - Artist name
        - Followers count
        - Monthly listeners (if available)
        - Popularity score
        - Genres
        - Extraction date
        - URL
        """
        import pandas as pd
        from datetime import datetime
        
        if not self.current_artist:
            print("❌ No artist data available")
            return None
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Get current date
        extraction_date = datetime.now().strftime("%Y-%m-%d")
        
        # Prepare artist statistics data
        artist_stats = {
            "Extraction Date": [extraction_date],
            "Artist Name": [self.current_artist["name"]],
            "Monthly Listeners": [
                self.current_artist.get("monthly_listeners") if self.current_artist.get("monthly_listeners") else "N/A"
            ],
            "Followers": [self.current_artist["followers"]],
            "Popularity Score": [self.current_artist["popularity"]],
            "Genres": [", ".join(self.current_artist["genres"]) if self.current_artist["genres"] else "N/A"],
            "Spotify URL": [self.current_artist["url"]]
        }
        
        # Create DataFrame
        df = pd.DataFrame(artist_stats)
        
        # Generate filename
        if filename is None:
            artist_name = self.current_artist["name"]
            clean_name = artist_name.replace(' ', '_').lower()
            
            # Add date if requested
            if include_date:
                date_str = datetime.now().strftime("%Y%m%d")
                filename = f"{clean_name}_artist_stats_{date_str}.xlsx"
            else:
                filename = f"{clean_name}_artist_stats.xlsx"
        
        filepath = os.path.join(output_dir, filename)
        
        # Save to Excel
        df.to_excel(filepath, index=False)
        print(f"📊 Artist statistics saved to: {filepath}")
        
        return filepath
    
    def analyze_artist(self, artist_name: str, country: str = "US") -> Dict:
        """Complete analysis of an artist"""
        print(f"🔍 Searching for artist: {artist_name}")
        
        # Find artist
        artist = self.find_artist(artist_name)
        if not artist:
            raise ValueError(f"Artist not found: {artist_name}")
        
        print(f"✅ Found artist: {artist['name']}")
        print("📊 Fetching comprehensive data...")
        
        # Get all data
        top_tracks = self.get_top_tracks(country=country)
        albums = self.get_albums()
        related_artists = self.get_related_artists()
        
        # Compile data
        self.current_data = {
            "artist": artist,
            "top_tracks": top_tracks,
            "albums": albums,
            "related_artists": related_artists,
            "search_query": artist_name,
            "country_market": country
        }
        
        return self.current_data
    
    def save_data(self, filename: str = None, data: Dict = None, output_dir: str = "result", include_date: bool = False) -> str:
        """Save analysis data to JSON"""
        data = data or self.current_data
        if not data:
            raise ValueError("No data to save. Run analyze_artist() first.")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        if filename is None:
            artist_name = data["artist"]["name"]
            clean_name = "".join(c for c in artist_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_name = clean_name.replace(' ', '_').lower()
            
            # Add date if requested
            if include_date:
                from datetime import datetime
                date_str = datetime.now().strftime("%Y%m%d")
                filename = f"{clean_name}_{date_str}.json"
            else:
                filename = f"spotify_artist_data_{clean_name}.json"
        
        # Save to output directory
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def print_stats(self, data: Dict = None):
        """Print formatted statistics (without duration info)"""
        data = data or self.current_data
        if not data:
            raise ValueError("No data to display. Run analyze_artist() first.")
        
        artist = data["artist"]
        
        print("=" * 60)
        print(f"🎵 ARTIST: {artist['name']}")
        print("=" * 60)
        print(f"📊 Popularity Score: {artist['popularity']}/100")
        print(f"👥 Followers: {artist['followers']:,}")
        if artist.get('monthly_listeners'):
            print(f"🎧 Monthly Listeners: {artist['monthly_listeners']:,}")
        print(f"🎭 Genres: {', '.join(artist['genres'])}")
        print(f"🔗 Spotify URL: {artist['url']}")
        
        print("\n" + "=" * 60)
        print("🎵 TOP TRACKS")
        print("=" * 60)
        
        for i, track in enumerate(data["top_tracks"], 1):
            print(f"{i:2d}. {track['name']}")
            print(f"    📊 Popularity: {track['popularity']}/100")
            # Duration info removed
            print(f"    💿 Album: {track['album']['name']} ({track['album']['release_date']})")
            print()
        
        print("=" * 60)
        print("💿 RECENT ALBUMS/SINGLES")
        print("=" * 60)
        
        for album in data["albums"][:5]:
            print(f"📀 {album['name']}")
            print(f"   📅 Released: {album['release_date']}")
            print(f"   🎵 Tracks: {album['total_tracks']}")
            print(f"   📂 Type: {album['album_type'].title()}")
            print()
    

    def create_visualizations(self, output_dir: str = "result", custom_name: str = None, include_date: bool = False):
        """Create visualizations using matplotlib and pandas (popularity only)"""
        try:
            import matplotlib.pyplot as plt
            import pandas as pd
            import matplotlib.font_manager as fm
            
            # Configure Chinese font support
            plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False  # Fix minus sign display
            
            if not self.current_data:
                raise ValueError("No data to visualize. Run analyze_artist() first.")
            
            # Create output directory in current working directory
            os.makedirs(output_dir, exist_ok=True)
            print(f"📁 Output directory: {os.path.abspath(output_dir)}")
            
            data = self.current_data
            tracks = data["top_tracks"]
            artist_name = data["artist"]["name"]
            
            # Generate base name
            if custom_name:
                base_name = custom_name
            else:
                base_name = artist_name.replace(' ', '_').lower()
            
            # Add date if requested
            if include_date:
                from datetime import datetime
                date_str = datetime.now().strftime("%Y%m%d")
                base_name = f"{base_name}_{date_str}"
            
            if not tracks:
                print("❌ No track data available for visualization")
                return None
            
            print("🎨 Creating visualizations...")
            
            # Prepare data
            track_names = [t["name"] for t in tracks]
            popularities = [t["popularity"] for t in tracks]
            
            # Popularity Chart Only
            plt.figure(figsize=(12, 8))
            bars = plt.barh(track_names, popularities, color='lightseagreen', alpha=0.8)
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'{width}', ha='left', va='center', fontweight='bold')
            
            plt.xlabel('Popularity Score', fontsize=12, fontweight='bold')
            plt.ylabel('Track', fontsize=12, fontweight='bold')
            plt.title(f'{artist_name} - Top Tracks Popularity', fontsize=16, fontweight='bold')
            plt.gca().invert_yaxis()
            plt.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            
            # Save popularity chart with custom name
            popularity_file = os.path.join(output_dir, f"{base_name}_popularity.png")
            plt.savefig(popularity_file, dpi=300, bbox_inches='tight')
            print(f"📊 Popularity chart saved: {popularity_file}")
            # plt.show()  # Commented out to save without displaying
            plt.close()
            
            # Duration chart removed
            
            # Create Excel summary (without duration)
            df = pd.DataFrame([
                {
                    "Track": t["name"],
                    "Popularity": t["popularity"],
                    "Album": t["album"]["name"],
                    "Release Date": t["album"]["release_date"]
                } for t in tracks
            ])
            
            excel_file = os.path.join(output_dir, f"{base_name}_top_tracks.xlsx")
            df.to_excel(excel_file, index=False)
            print(f"📋 Excel file saved: {excel_file}")
            
            print("✅ Visualizations created successfully!")
            
            return {
                "popularity_chart": popularity_file,
                "excel_file": excel_file
            }
            
        except ImportError:
            print("❌ Visualization dependencies not available. Install matplotlib and pandas:")
            print("pip install matplotlib pandas openpyxl")
            return None
        except Exception as e:
            import traceback
            print(f"❌ Error creating visualizations: {e}")
            traceback.print_exc()
            return None

def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description="Comprehensive Spotify Artist Analysis Tool",
        epilog="""
Examples:
  # Basic analysis with charts and artist stats
  python %(prog)s "Tom Misch" --charts
  
  # Specify monthly listeners manually (from Spotify website)
  python %(prog)s "Tom Misch" --monthly-listeners 5000000 --charts
  
  # Get all songs from an artist
  python %(prog)s "Tom Misch" --all-songs
  
  # Get all songs from 2020 onwards
  python %(prog)s "Tom Misch" --all-songs --from-date 2020
  
  # Full analysis with date-stamped files and manual monthly listeners
  python %(prog)s "Tom Misch" --all-songs --charts --add-date --monthly-listeners 5000000

Note: Artist statistics (followers, popularity, genres, extraction date) 
      are automatically saved to Excel for all analyses.
      Monthly listeners data is NOT available via Spotify API - you can 
      manually specify it using --monthly-listeners option.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("artist", 
                       help="Name of the artist to analyze (e.g., 'Tom Misch', 'Frankfurt Helmet')")
    
    parser.add_argument("--country", 
                       default="US", 
                       metavar="CODE",
                       help="Country market code for top tracks (default: US). Examples: GB, DE, JP, CN")
    
    parser.add_argument("--no-save", 
                       action="store_true", 
                       help="Don't save JSON data file to disk")
    
    parser.add_argument("--charts", 
                       action="store_true", 
                       help="Create and save popularity visualization charts (PNG files)")
    
    parser.add_argument("--output-dir", 
                       default="result", 
                       metavar="DIR",
                       help="Output directory for all files (default: result/)")
    
    parser.add_argument("--all-songs", 
                       action="store_true", 
                       help="Fetch ALL songs from artist's entire discography (not just top 10 tracks). This will create a comprehensive Excel file with all songs and their popularity scores.")
    
    parser.add_argument("--from-date", 
                       type=str, 
                       metavar="DATE",
                       help="Filter songs/albums from this date onwards. Format: YYYY (e.g., 2020) or YYYY-MM-DD (e.g., 2020-04-24). Only works with --all-songs option.")
    
    parser.add_argument("--output-name", 
                       type=str, 
                       metavar="NAME",
                       help="Custom base name for output files (without extension). If not specified, artist name will be used. Example: --output-name my_analysis")
    
    parser.add_argument("--add-date", 
                       action="store_true", 
                       help="Add current date (YYYYMMDD) to all output filenames. Example: tom_misch_20251008.json")
    
    parser.add_argument("--monthly-listeners", 
                       type=int, 
                       metavar="NUMBER",
                       help="Manually specify monthly listeners count (e.g., --monthly-listeners 5000000). This data is not available via Spotify API and must be obtained from the Spotify web interface.")
    
    args = parser.parse_args()
    
    try:
        # Validate from-date usage
        if args.from_date and not args.all_songs:
            print("⚠️  Warning: --from-date option only works with --all-songs. Ignoring date filter.")
            print("    Use: --all-songs --from-date 2020\n")
        
        # Initialize analyzer
        print("🎵 Spotify Artist Analyzer")
        print("="*60)
        analyzer = SpotifyArtistAnalyzer()
        
        # Analyze artist
        data = analyzer.analyze_artist(args.artist, args.country)
        
        # Override monthly listeners if manually specified
        if args.monthly_listeners:
            analyzer.current_artist["monthly_listeners"] = args.monthly_listeners
            print(f"✅ Monthly listeners manually set to: {args.monthly_listeners:,}")
        
        # Create artist-specific subfolder
        artist_name = data["artist"]["name"]
        clean_artist_name = "".join(c for c in artist_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_artist_name = clean_artist_name.replace(' ', '_')
        
        # Create artist folder under output directory
        artist_folder = os.path.join(args.output_dir, clean_artist_name)
        os.makedirs(artist_folder, exist_ok=True)
        
        print(f"📁 Artist folder created: {os.path.abspath(artist_folder)}")
        print()
        
        # Display results
        analyzer.print_stats()
        
        # Save data
        if not args.no_save:
            # Custom filename for JSON
            if args.output_name:
                if args.add_date:
                    from datetime import datetime
                    date_str = datetime.now().strftime("%Y%m%d")
                    json_filename = f"{args.output_name}_{date_str}.json"
                else:
                    json_filename = f"{args.output_name}.json"
            else:
                json_filename = None
            
            filename = analyzer.save_data(filename=json_filename, output_dir=artist_folder, include_date=args.add_date)
            print(f"💾 Data saved to: {filename}")
        
        # Get all songs if requested
        if args.all_songs:
            print("\n" + "="*60)
            print("🎵 FETCHING ALL SONGS FROM ENTIRE DISCOGRAPHY")
            if args.from_date:
                print(f"📅 Filtering: Albums/songs from {args.from_date} onwards")
            print("="*60)
            
            all_songs = analyzer.get_all_songs(from_date=args.from_date)
            
            if all_songs:
                # Generate filenames with date if requested
                if args.add_date:
                    from datetime import datetime
                    date_str = datetime.now().strftime("%Y%m%d")
                else:
                    date_str = None
                
                # Save all songs to Excel
                if args.output_name:
                    if date_str:
                        excel_filename = f"{args.output_name}_all_songs_{date_str}.xlsx"
                        json_all_filename = f"{args.output_name}_all_songs_{date_str}.json"
                    else:
                        excel_filename = f"{args.output_name}_all_songs.xlsx"
                        json_all_filename = f"{args.output_name}_all_songs.json"
                else:
                    excel_filename = None
                    json_all_filename = None
                
                excel_path = analyzer.save_all_songs_to_excel(
                    all_songs, 
                    output_dir=artist_folder,
                    filename=excel_filename,
                    include_date=args.add_date
                )
                
                # Save all songs to JSON
                if json_all_filename is None:
                    artist_name_clean = clean_artist_name.lower()
                    if date_str:
                        json_all_filename = f"{artist_name_clean}_all_songs_{date_str}.json"
                    else:
                        json_all_filename = f"{artist_name_clean}_all_songs.json"
                
                json_all_path = os.path.join(artist_folder, json_all_filename)
                with open(json_all_path, 'w', encoding='utf-8') as f:
                    json.dump(all_songs, f, indent=2, ensure_ascii=False)
                
                print(f"\n✅ SUCCESS! All songs saved")
                print(f"   📊 Total songs found: {len(all_songs)}")
                print(f"   📁 Excel file: {excel_path}")
                print(f"   📁 JSON file: {json_all_path}")
        
        # Save artist statistics to Excel (always include date)
        print("\n" + "="*60)
        print("📊 SAVING ARTIST STATISTICS")
        print("="*60)
        
        # Custom filename for artist stats
        if args.output_name:
            if args.add_date:
                from datetime import datetime
                date_str = datetime.now().strftime("%Y%m%d")
                stats_filename = f"{args.output_name}_artist_stats_{date_str}.xlsx"
            else:
                stats_filename = f"{args.output_name}_artist_stats.xlsx"
        else:
            stats_filename = None
        
        stats_path = analyzer.save_artist_stats_to_excel(
            output_dir=artist_folder,
            filename=stats_filename,
            include_date=args.add_date or True  # Always include date by default
        )
        
        print(f"📁 Artist stats file: {stats_path}")
        
        # Create charts
        if args.charts:
            print()
            analyzer.create_visualizations(artist_folder, custom_name=args.output_name, include_date=args.add_date)
        
        print("\n" + "="*60)
        print("✅ Analysis complete!")
        print("="*60)
        
    except Exception as e:
        import traceback
        print(f"\n❌ Error: {e}")
        print("\nFor help, run: python spotify_artist_stats_and_visul_fetch.py --help")
        traceback.print_exc()

if __name__ == "__main__":
    main()