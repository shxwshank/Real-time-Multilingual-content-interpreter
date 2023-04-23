from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from bson import json_util
import requests 
import os
from google.cloud import translate_v2 as translate


@csrf_exempt
def get_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            song_name = data['songname']
            artist_name = data ['artistname']
            # Create message object
            trly = crazy(song_name,artist_name)
            ly = get_lyrics(song_name,artist_name)
            Songs = {
                'songname': song_name,
                'artistname': artist_name,
                # 'lyrics': 'lyrics',
                # 'translatedlyrics': 'translatedlyrics'
            }
            print(Songs)

            
            return JsonResponse({'status': 'success', 'lyrics': ly, 'translated_lyrics': trly}, safe=False)
        except:
            return HttpResponseBadRequest('Invalid request data')
    else:
        return HttpResponseBadRequest('Invalid request method')
    




MUSIXMATCH_API_KEY = "8c68f735e02b07f1852aacb89ef39a16"

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
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/apple/Downloads/IR/backend/ir-translate-4ee52989ff7a.json"
    translate_client = translate.Client()
    target = dest_lang

    result = translate_client.translate(text, target_language=target)
    return result['translatedText'].replace("&#39;", "'")

def crazy(songname, artistname):
    res= translate_text(get_lyrics(songname, artistname), "en")
    return res

# @csrf_exempt
# def send_lyrics(request, song_name, artist_name):
#     if request.method == 'POST':
#         try:
#             res= translate_text(get_lyrics(song_name, artist_name), "en")
#             return JsonResponse({'status': 'success', 'message': 'Message received'}, safe=False)
#         except:
#             return HttpResponseBadRequest('Invalid request data')
#     else:
#         return HttpResponseBadRequest('Invalid request method')
@csrf_exempt

def getreqlyrics(request):
    lyrics = ly
    translated_lyrics = trly
    data = {'lyrics': lyrics, 'translated_lyrics': translated_lyrics}
    return JsonResponse(data)
