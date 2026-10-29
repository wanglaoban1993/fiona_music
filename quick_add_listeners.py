"""
快速添加月活跃听众数据工具
Quick tool to add monthly listeners data

使用方法 / Usage:
    python quick_add_listeners.py

这个脚本会：
1. 询问艺术家名称
2. 询问月活跃听众数（从Spotify网页查看）
3. 自动生成并运行完整的分析命令
"""

import subprocess
import sys

def main():
    print("=" * 60)
    print("🎵 Spotify艺术家数据提取工具")
    print("   Quick Artist Data Extraction Tool")
    print("=" * 60)
    print()
    
    # 获取艺术家名称
    artist_name = input("请输入艺术家名称 (Artist name): ").strip()
    if not artist_name:
        print("❌ 艺术家名称不能为空！")
        return
    
    print()
    print("=" * 60)
    print("📊 获取月活跃听众数 (Get Monthly Listeners)")
    print("=" * 60)
    print()
    print("请访问Spotify网页查看艺术家的月活跃听众数：")
    print(f"🔗 https://open.spotify.com/search/{artist_name.replace(' ', '%20')}")
    print()
    print("在艺术家页面可以看到类似 '500,000 monthly listeners' 的文字")
    print()
    
    # 获取月活跃听众数
    while True:
        listeners_input = input("月活跃听众数 (输入数字，不知道请按Enter跳过): ").strip()
        
        if not listeners_input:
            monthly_listeners = None
            print("⚠️  未指定月活跃听众数，将在Excel中显示 'N/A'")
            break
        
        try:
            # 移除可能的逗号
            listeners_input = listeners_input.replace(',', '').replace('.', '')
            monthly_listeners = int(listeners_input)
            print(f"✅ 月活跃听众数: {monthly_listeners:,}")
            break
        except ValueError:
            print("❌ 请输入有效的数字！")
    
    print()
    print("=" * 60)
    print("⚙️  分析选项 (Analysis Options)")
    print("=" * 60)
    print()
    
    # 询问是否获取所有歌曲
    all_songs = input("是否获取所有歌曲？[y/N]: ").strip().lower() == 'y'
    
    # 询问是否生成图表
    charts = input("是否生成可视化图表？[y/N]: ").strip().lower() == 'y'
    
    print()
    print("=" * 60)
    print("🚀 开始分析... (Starting analysis...)")
    print("=" * 60)
    print()
    
    # 构建命令
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
    
    # 显示将要执行的命令
    print("执行命令 (Command):")
    print(" ".join(cmd))
    print()
    
    # 执行命令
    try:
        result = subprocess.run(cmd, check=True)
        print()
        print("=" * 60)
        print("✅ 分析完成！(Analysis complete!)")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print(f"❌ 错误: {e}")
        print("=" * 60)
    except KeyboardInterrupt:
        print()
        print("⚠️  用户取消操作")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  操作已取消")
        sys.exit(0)
