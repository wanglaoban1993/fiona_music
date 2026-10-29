# 🎵 Spotify艺术家数据提取功能完整说明

## 📊 更新内容（2025-10-08）

现在脚本可以提取并保存以下完整的艺术家统计数据到Excel文件：

### ✅ 自动提取的数据（通过API）

1. **艺术家名称** (Artist Name)
2. **粉丝数量** (Followers Count) - Spotify粉丝总数
3. **流行度分数** (Popularity Score) - 0-100评分
4. **音乐类型** (Genres) - 所有音乐风格
5. **Spotify URL** - 艺术家页面链接
6. **提取日期** (Extraction Date) - 自动记录

### ⭐ 手动添加的数据

7. **月活跃听众** (Monthly Listeners) - 需要从Spotify网页手动查看并输入

---

## 🚀 三种使用方法

### 方法1：快速交互式工具（最简单）✨

```bash
python quick_add_listeners.py
```

**优点**：
- 交互式提示，无需记忆复杂命令
- 自动打开Spotify搜索链接
- 引导式输入月活跃听众数

**使用流程**：
1. 运行脚本
2. 输入艺术家名称
3. 访问提供的Spotify链接
4. 输入看到的月活跃听众数
5. 选择是否需要完整分析
6. 自动生成所有文件

---

### 方法2：命令行（完整控制）

#### 基本用法

```bash
python test\spotify_artist_stats_and_visul_fetch.py "艺术家名称" --monthly-listeners 数字
```

#### 完整示例

```bash
# Venna - 包含所有功能
python test\spotify_artist_stats_and_visul_fetch.py "Venna" \
    --monthly-listeners 500000 \
    --all-songs \
    --charts \
    --add-date

# Tom Misch - 仅基本统计和图表
python test\spotify_artist_stats_and_visul_fetch.py "Tom Misch" \
    --monthly-listeners 5200000 \
    --charts \
    --add-date

# 周杰伦 - 完整分析
python test\spotify_artist_stats_and_visul_fetch.py "周杰伦" \
    --monthly-listeners 10000000 \
    --all-songs \
    --charts \
    --add-date
```

---

### 方法3：不指定月活跃听众

```bash
# 如果暂时没有月活跃听众数据，可以不指定
python test\spotify_artist_stats_and_visul_fetch.py "艺术家名称" --charts --add-date

# Excel中会显示 "N/A"
```

---

## 📁 输出文件结构

运行后会在 `result/艺术家名称/` 文件夹中生成：

```
result/
└── Venna/
    ├── venna_artist_stats_20251008.xlsx    ⭐ 艺术家统计（含月活跃听众）
    ├── venna_20251008.json                  完整JSON数据
    ├── venna_20251008_popularity.png        流行度图表（--charts）
    ├── venna_20251008_top_tracks.xlsx       Top曲目列表（--charts）
    ├── venna_all_songs_20251008.xlsx        所有歌曲列表（--all-songs）
    └── venna_all_songs_20251008.json        所有歌曲JSON（--all-songs）
```

---

## 📊 Excel统计文件详细说明

### 文件名
- 格式：`artistname_artist_stats_YYYYMMDD.xlsx`
- 示例：`venna_artist_stats_20251008.xlsx`

### 包含的列

| 列名（中英文） | 数据来源 | 示例值 |
|--------------|---------|--------|
| 提取日期 (Extraction Date) | 自动生成 | 2025-10-08 |
| 艺术家名称 (Artist Name) | Spotify API | Venna |
| 月活跃听众 (Monthly Listeners) | 手动输入 | 500,000 |
| 粉丝数量 (Followers) | Spotify API | 78,294 |
| 流行度分数 (Popularity Score) | Spotify API | 58 |
| 音乐类型 (Genres) | Spotify API | jazz rap, uk r&b |
| Spotify URL | Spotify API | https://open.spotify.com/artist/... |

---

## 🔍 如何获取月活跃听众数

### 步骤：

1. **打开Spotify网页版**
   ```
   https://open.spotify.com
   ```

2. **搜索艺术家**
   - 在搜索框输入艺术家名称
   - 点击艺术家进入主页

3. **查看数据**
   - 在艺术家照片下方，名字旁边会显示：
     ```
     500,000 monthly listeners
     ```

4. **记录数字**
   - 复制数字（去掉逗号）
   - 500,000 → 输入 `500000`

### 快捷链接：

```
https://open.spotify.com/search/艺术家名称
```

---

## ⚙️ 所有命令参数说明

| 参数 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| `艺术家名称` | 必需 | 要分析的艺术家 | `"Venna"` |
| `--monthly-listeners` | 可选 | 手动指定月活跃听众数 | `--monthly-listeners 500000` |
| `--charts` | 可选 | 生成可视化图表（PNG + Excel） | `--charts` |
| `--all-songs` | 可选 | 获取所有歌曲（而非仅top 10） | `--all-songs` |
| `--add-date` | 可选 | 文件名添加日期（推荐） | `--add-date` |
| `--from-date` | 可选 | 只获取指定日期后的歌曲 | `--from-date 2020` |
| `--output-name` | 可选 | 自定义输出文件名 | `--output-name my_analysis` |
| `--country` | 可选 | 指定国家市场代码 | `--country US` |

---

## 💡 最佳实践

### 推荐配置：

```bash
python test\spotify_artist_stats_and_visul_fetch.py "艺术家名称" \
    --monthly-listeners 从Spotify查看的数字 \
    --all-songs \
    --charts \
    --add-date
```

这样可以获得：
- ✅ 完整的艺术家统计（含月活跃听众）
- ✅ 所有歌曲列表
- ✅ 可视化图表
- ✅ 带日期的文件名（方便追踪）

### 定期更新：

```bash
# 每周/每月重新运行，追踪数据变化
python test\spotify_artist_stats_and_visul_fetch.py "Venna" \
    --monthly-listeners 最新数字 \
    --charts \
    --add-date
```

由于使用了 `--add-date`，每次运行都会生成新文件，不会覆盖旧数据。

---

## 📝 实际使用案例

### 案例1：分析新艺术家Venna

```bash
# 1. 访问 Spotify 查看 Venna
# 链接：https://open.spotify.com/artist/7qKJMpPZfyGHHwPgsjgFCP

# 2. 看到：500,000 monthly listeners

# 3. 运行分析
python test\spotify_artist_stats_and_visul_fetch.py "Venna" \
    --monthly-listeners 500000 \
    --all-songs \
    --charts \
    --add-date

# 4. 查看结果
# result/Venna/venna_artist_stats_20251008.xlsx
```

**输出数据**：
- 月活跃听众: 500,000
- 粉丝数量: 78,294
- 流行度: 58/100
- 类型: jazz rap, uk r&b

---

### 案例2：追踪Tom Misch的数据变化

```bash
# 第一次（2025-10-08）
python test\spotify_artist_stats_and_visul_fetch.py "Tom Misch" \
    --monthly-listeners 5200000 \
    --charts \
    --add-date

# 一个月后（2025-11-08）
python test\spotify_artist_stats_and_visul_fetch.py "Tom Misch" \
    --monthly-listeners 5500000 \
    --charts \
    --add-date

# 结果：两个文件可以对比
# - tom_misch_artist_stats_20251008.xlsx
# - tom_misch_artist_stats_20251108.xlsx
```

---

## 🆘 常见问题

### Q1: 为什么月活跃听众不能自动获取？
**A**: Spotify官方API不提供这个数据。这是Spotify网页端专有的统计数据，只能手动查看。

### Q2: 不输入月活跃听众会怎样？
**A**: Excel文件中"月活跃听众"列会显示 "N/A"，其他数据正常显示。

### Q3: 月活跃听众数字要加逗号吗？
**A**: 不需要。输入纯数字即可，例如 `500000` 而不是 `500,000`。

### Q4: 数据多久更新一次？
**A**: 
- **粉丝数、流行度**：实时数据，建议每周更新
- **月活跃听众**：每天变化，建议定期记录

### Q5: 如何批量分析多个艺术家？
**A**: 可以使用Windows批处理脚本：

```batch
@echo off
python test\spotify_artist_stats_and_visul_fetch.py "Venna" --monthly-listeners 500000 --charts --add-date
python test\spotify_artist_stats_and_visul_fetch.py "Tom Misch" --monthly-listeners 5200000 --charts --add-date
python test\spotify_artist_stats_and_visul_fetch.py "周杰伦" --monthly-listeners 10000000 --charts --add-date
```

---

## 📚 相关文档

- `艺术家统计功能说明.md` - 基础功能介绍
- `如何添加月活跃听众数据.md` - 月活跃听众详细说明
- `test/spotify_artist_stats_and_visul_fetch.py` - 主程序
- `quick_add_listeners.py` - 快速交互工具

---

## 🔧 技术支持

### 依赖包：

```bash
pip install requests python-dotenv pandas openpyxl matplotlib beautifulsoup4
```

### 环境配置：

确保 `.env` 文件包含Spotify API凭证：
```
SPOTIFY_CLIENT_ID=你的client_id
SPOTIFY_CLIENT_SECRET=你的client_secret
```

---

## ✨ 总结

现在你可以：

1. ✅ 自动提取艺术家的粉丝数、流行度、音乐类型
2. ✅ 手动添加月活跃听众数据
3. ✅ 所有数据保存到Excel文件，包含提取日期
4. ✅ 生成可视化图表
5. ✅ 获取艺术家所有歌曲列表
6. ✅ 定期追踪数据变化

**开始使用**：

```bash
# 最简单的方式
python quick_add_listeners.py

# 或完整命令
python test\spotify_artist_stats_and_visul_fetch.py "艺术家名称" \
    --monthly-listeners 数字 \
    --all-songs \
    --charts \
    --add-date
```

祝使用愉快！🎵
