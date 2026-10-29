"""
Quick tool to add monthly listeners data

Usage:
    python quick_add_listeners.py

This script will:
1. Ask for the artist name
2. Ask for the monthly listeners count (check it on the Spotify web page)
3. Build and run the full analysis command automatically
"""

import subprocess
import sys

def main():
    print("=" * 60)
    print("🎵 Spotify Artist Data Extraction Tool")
    print("   Quick Artist Data Extraction Tool")
    print("=" * 60)
    print()
    
    # Get the artist name
    artist_name = input("Enter the artist name: ").strip()
    if not artist_name:
        print("❌ Artist name cannot be empty!")
        return
    
    print()
    print("=" * 60)
    print("📊 Get Monthly Listeners")
    print("=" * 60)
    print()
    print("Please visit the Spotify web page to check the artist's monthly listeners:")
    print(f"🔗 https://open.spotify.com/search/{artist_name.replace(' ', '%20')}")
    print()
    print("On the artist page you will see text like '500,000 monthly listeners'")
    print()
    
    # Get the monthly listeners count
    while True:
        listeners_input = input("Monthly listeners (enter a number, or press Enter to skip): ").strip()
        
        if not listeners_input:
            monthly_listeners = None
            print("⚠️  No monthly listeners specified; 'N/A' will be shown in Excel")
            break
        
        try:
            # Remove possible separators
            listeners_input = listeners_input.replace(',', '').replace('.', '')
            monthly_listeners = int(listeners_input)
            print(f"✅ Monthly listeners: {monthly_listeners:,}")
            break
        except ValueError:
            print("❌ Please enter a valid number!")
    
    print()
    print("=" * 60)
    print("⚙️  Analysis Options")
    print("=" * 60)
    print()
    
    # Ask whether to fetch all songs
    all_songs = input("Fetch all songs? [y/N]: ").strip().lower() == 'y'
    
    # Ask whether to generate charts
    charts = input("Generate visualization charts? [y/N]: ").strip().lower() == 'y'
    
    print()
    print("=" * 60)
    print("🚀 Starting analysis...")
    print("=" * 60)
    print()
    
    # Build the command
    cmd = [
        "python",
        "test/spotify_artist_stats_and_visul_fetch.py",
        artist_name,
        "--add-date"
    ]
    
    if monthly_listeners is not None:
        cmd.extend(["--monthly-listeners", str(monthly_listeners)])
    
    if all_songs:
        cmd.append("--all-songs")
    
    if charts:
        cmd.append("--charts")
    
    # Show the command to be executed
    print("Command:")
    print(" ".join(cmd))
    print()
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=True)
        print()
        print("=" * 60)
        print("✅ Analysis complete!")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print(f"❌ Error: {e}")
        print("=" * 60)
    except KeyboardInterrupt:
        print()
        print("⚠️  Cancelled by user")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled")
        sys.exit(0)
