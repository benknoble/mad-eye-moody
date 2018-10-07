import spotipy
import os
from spotipy import oauth2
import json

mood_filters = {
        'happy': {
            'valence': (5, 10),
            'energy': (5, 10)
            },
        'sad': {
            'valence': (0, 5),
            'energy': (0, 5)
            },
        'peaceful': {
            'valence': (5, 10),
            'energy': (0, 5)
            },
        'angry': {
            'valence': (0, 5),
            'energy': (5, 10)
            },
        }

def generate_token(code,scope):
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

    if not client_id:
        print('''
            You need to set your Spotify API credentials. You can do this by
            setting environment variables like so:
            export SPOTIPY_CLIENT_ID='your-spotify-client-id'
            export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
            export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
            Get your credentials at     
                https://developer.spotify.com/my-applications
        ''')
        raise spotipy.SpotifyException(550, -1, 'no credentials set')

    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=scope)
    return sp_oauth.get_access_token(code)['access_token']

def get_playlist_tracks(token):
    sp = spotipy.Spotify(auth=token)

    user_id = sp.me()['id']
    playlists = sp.user_playlists(user=user_id)

    tracks = set()
    for playlist in playlists['items']:
        playlist_tracks = sp.user_playlist_tracks(user=user_id,playlist_id=playlist['id'])
        for track in playlist_tracks['items']:
            tracks.add(track["track"]["id"])

    tracks = list(filter(lambda x: x is not None, tracks))
    return list(tracks)

def get_track_data(track_ids, token):
    sp = spotipy.Spotify(auth=token)

    total_track_data = []
    while len(track_ids) > 0:
        total_track_data = total_track_data + sp.audio_features(track_ids[:50])
        track_ids = track_ids[50:]
    
    return total_track_data

def create_playlist(name, track_ids, token):
    sp = spotipy.Spotify(auth=token)
    user_id = sp.me()['id']

    created_playlist = sp.user_playlist_create(user=user_id,name=name)
    playlist_id = created_playlist['id']

    while len(track_ids) > 0:
        sp.user_playlist_add_tracks(user=user_id,playlist_id=playlist_id,tracks=track_ids[:100])
        track_ids = track_ids[100:]

    return playlist_id

def filter_tracks(mood, track_data):
    result = []
    if mood in mood_filters.keys():
        filters = mood_filters[mood]
        for track in track_data:
            if all([low <= 10*track.get(attr) <= high
                    for (attr, (low, high)) in filters.items()]):
                result.append(track['id'])
        return result
    else:
        print(f'Bad mood: {mood}')
        return []
