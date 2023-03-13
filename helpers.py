import requests 
import json
from dotenv import load_dotenv
import os
from google.cloud import translate_v2 as translate

load_dotenv()

MUSIXMATCH_API_KEY = os.getenv("MUSIXMATCH_API_KEY")

def search_song(song_name, author_name=None):
    """
    Given a song name and an artist name, returns a unique ID for the song
    """
    params={
        'apikey': MUSIXMATCH_API_KEY,
        'q_track': song_name,
        's_track_rating': 'desc',
        'f_has_lyrics': '1'
    }
    if author_name:
        params['q_artist'] = author_name
    r = requests.get('http://api.musixmatch.com/ws/1.1/track.search', params=params).json()
    r=r["message"]["body"]
    return r["track_list"][0]["track"]["commontrack_id"]

def song_id_to_lyrics(track_id):
    """
    Given a unique ID for the song, returns the lyrics of the song as a string
    """
    r = requests.get('http://api.musixmatch.com/ws/1.1/track.lyrics.get', params={
        'apikey': MUSIXMATCH_API_KEY,
        'commontrack_id': track_id
    }).json()
    lyric = r["message"]["body"]
    lyric = lyric["lyrics"]["lyrics_body"]
    lyric = lyric.replace("******* This Lyrics is NOT for Commercial use *******", "")
    lyric = lyric.replace("(", "")
    lyric = lyric.replace(")", "")
    lyric = lyric.replace("...", "")
    return ' '.join(lyric.split('\n')[1:-1])

def get_lyrics(song_name, author_name=""):
    """
    Returns the lyrics of the song as a string for a provided song_name. author_name is optional.
    """
    track_id = search_song(song_name, author_name)
    lyrics = song_id_to_lyrics(track_id)
    return lyrics

def translate_text(text, dest_lang):
    """"
    Translates the passed text to the destination language "dest_lang"
    """
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(curr_dir, 'service-cred.json')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=file_path
    translate_client = translate.Client()
    target = dest_lang

    result = translate_client.translate(text, target_language=target)
    return result['translatedText'].replace("&#39;", "'")


def userinput():
    songname = input("Enter the name of the song:")
    artistname = input("Enter the name of the artist:")
    if len(artistname)==0:
        artistname=None
    res= translate_text(get_lyrics(songname, artistname), "en")
    print(res)

if __name__ == "__main__":
    userinput()