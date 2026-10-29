"""
测试脚本：提取艺术家统计数据
Test script: Extract artist statistics including followers and popularity
"""

import sys
import os

# Import the analyzer
from spotify_artist_stats_and_visul_fetch import SpotifyArtistAnalyzer

def test_artist_stats(artist_name: str):
    """Test extracting artist statistics"""
    
    print(f"🎵 测试艺术家统计数据提取")
    print(f"   Testing artist statistics extraction for: {artist_name}")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = SpotifyArtistAnalyzer()
    
    # Analyze artist
    print(f"🔍 搜索艺术家: {artist_name}")
    data = analyzer.analyze_artist(artist_name)
    
    # Display basic info
    artist = data["artist"]
    print(f"\n✅ 找到艺术家: {artist['name']}")
    print(f"   📊 流行度分数: {artist['popularity']}/100")
    print(f"   👥 粉丝数量: {artist['followers']:,}")
    print(f"   🎭 音乐类型: {', '.join(artist['genres'])}")
    
    # Save artist statistics to Excel
    print(f"\n💾 保存艺术家统计数据到 Excel...")
    stats_file = analyzer.save_artist_stats_to_excel(
        output_dir="result/test",
        include_date=True
    )
    
    print(f"\n✅ 完成!")
    print(f"   📁 统计文件已保存到: {stats_file}")
    print("\n说明 (Notes):")
    print("   - Excel文件包含提取日期 (Excel file includes extraction date)")
    print("   - 包含粉丝数量 (Includes follower count)")
    print("   - 包含流行度分数 (Includes popularity score)")
    print("   - 包含音乐类型 (Includes genres)")

if __name__ == "__main__":
    # Test with a sample artist
    test_artist = "Tom Misch" if len(sys.argv) < 2 else sys.argv[1]
    test_artist_stats(test_artist)
