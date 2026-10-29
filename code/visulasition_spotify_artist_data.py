import json
import pandas as pd
import matplotlib.pyplot as plt

# 1. Read JSON file
with open("spotify_artist_data_frankfurt_helmet.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. Extract top tracks info
tracks = data["top_tracks"]
track_data = []
for t in tracks:
    track_data.append({
        "Name": t["name"],
        "Popularity": t["popularity"],
        "Duration_min": t["duration_min"],
        "Album": t["album"]["name"],
        "Release_Date": t["album"]["release_date"],
        "Artists": ", ".join(t["artists"])
    })

df = pd.DataFrame(track_data)

# 3. Save to Excel
excel_file = "spotify_top_tracks.xlsx"
df.to_excel(excel_file, index=False)
print(f"Saved top tracks to {excel_file}")

# 4. Plot popularity
plt.figure(figsize=(12, 8))
plt.barh(df["Name"], df["Popularity"], color="skyblue")
plt.xlabel("Popularity")
plt.ylabel("Track")
plt.title(f"Top Tracks Popularity - {data['artist']['name']}")
plt.gca().invert_yaxis()  # highest popularity at top
plt.tight_layout()

# Save the image first, then show it
plt.savefig("../result/top_tracks_popularity.png", dpi=300, bbox_inches='tight')
print("Saved popularity chart to ../result/top_tracks_popularity.png")
plt.show()
plt.close()