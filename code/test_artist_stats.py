"""
Test script: Extract artist statistics including followers and popularity
"""

import sys
import os

# Import the analyzer
from spotify_artist_stats_and_visul_fetch import SpotifyArtistAnalyzer

def test_artist_stats(artist_name: str):
    """Test extracting artist statistics"""
    
    print(f"🎵 Artist statistics extraction test")
    print(f"   Testing artist statistics extraction for: {artist_name}")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = SpotifyArtistAnalyzer()
    
    # Analyze artist
    print(f"🔍 Searching for artist: {artist_name}")
    data = analyzer.analyze_artist(artist_name)
    
    # Display basic info
    artist = data["artist"]
    print(f"\n✅ Artist found: {artist['name']}")
    print(f"   📊 Popularity score: {artist['popularity']}/100")
    print(f"   👥 Followers: {artist['followers']:,}")
    print(f"   🎭 Genres: {', '.join(artist['genres'])}")
    
    # Save artist statistics to Excel
    print(f"\n💾 Saving artist statistics to Excel...")
    stats_file = analyzer.save_artist_stats_to_excel(
        output_dir="result/test",
        include_date=True
    )
    
    print(f"\n✅ Done!")
    print(f"   📁 Statistics file saved to: {stats_file}")
    print("\nNotes:")
    print("   - Excel file includes extraction date")
    print("   - Includes follower count")
    print("   - Includes popularity score")
    print("   - Includes genres")

if __name__ == "__main__":
    # Test with a sample artist
    test_artist = "Tom Misch" if len(sys.argv) < 2 else sys.argv[1]
    test_artist_stats(test_artist)
