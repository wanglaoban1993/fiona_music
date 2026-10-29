import requests
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Get token
resp = requests.post('https://accounts.spotify.com/api/token', 
                     data={'grant_type': 'client_credentials'}, 
                     auth=(client_id, client_secret))
token = resp.json()['access_token']

# Search for artist
search_resp = requests.get('https://api.spotify.com/v1/search', 
                          headers={'Authorization': f'Bearer {token}'}, 
                          params={'q': 'Frankfurt Helmet', 'type': 'artist', 'limit': 10})

artists = search_resp.json()['artists']['items']

print('\n🔍 Search results for "Frankfurt Helmet":\n')
if artists:
    for i, a in enumerate(artists):
        print(f'{i+1}. Name: "{a["name"]}"')
        print(f'   Followers: {a["followers"]["total"]:,}')
        print(f'   Popularity: {a["popularity"]}/100')
        print(f'   ID: {a["id"]}')
        print()
else:
    print('❌ No results found')
