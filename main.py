import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
user_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

SPOTIFY_CLIENT_ID = "YOUR SPOTIFY CLIENT ID"
SPOTIFY_ID = "YOUR SPOTIFY ID"
USER_ID = "YOUR ID"
REDIRECT_URI = "https://www.example.com"
# This is the website where we scrape the 100 song of your giving date
billboard_url = f"https://www.billboard.com/charts/hot-100/{user_input}"
billboard_web = requests.get(url=billboard_url)
scope = "playlist-modify-private"

uris = []
sp = spotipy.Spotify(
auth_manager=SpotifyOAuth(
client_id=SPOTIFY_ID,
client_secret=SPOTIFY_CLIENT_ID,
redirect_uri=REDIRECT_URI,
show_dialog=True,
scope=scope,
cache_path="token.txt"))
soup = BeautifulSoup(billboard_web.text,'html.parser')
# song_titles = soup.select(selector="li h3")
song_artist_names = soup.find_all(name="span",class_="a-truncate-ellipsis-2line")
song_titles = soup.find_all(name="h3",class_="lrv-u-font-size-18@tablet")
# print(song_titles)
artists_names = [name.getText() for name in song_artist_names]
titles = [title.getText() for title in song_titles]
artists = [artists_names[n].strip() for n in range(1,len(artists_names))]
titles_music = [title.strip() for title in titles]
for n in range(len(artists)):
    result = sp.search(q=f"{artists[n]} {titles_music[n]}",type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uris.append(uri)
    except IndexError:
        print(f"{artists[n]} {titles_music[n]} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user="your id on spotify",name=f"{user_input} Billboard 100",public=False)

sp.user_playlist_add_tracks(user="your id on spotify",playlist_id=f"{playlist['id']}",tracks=uris)
