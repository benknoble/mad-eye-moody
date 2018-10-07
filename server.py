import os
import flask
from flask import request, render_template, send_file, redirect
from urllib import parse
import spotify_service
import json

# Heroku config vars
debug = (os.environ.get('DEBUG', 'True') == 'True')
port = os.environ.get('PORT', 8080)
spotipy_client_id = os.environ.get('SPOTIPY_CLIENT_ID')
spotipy_client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
spotipy_redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI', "http://www.madeyemoodify.com")
scope = 'user-library-read,playlist-read-private,playlist-modify-public'

app = flask.Flask(__name__)


@app.route('/')
@app.route("/callback")
def index():
    token = request.args.get('code')
    if token:
        return send_file("index.html")
    else:
        return redirect("https://accounts.spotify.com/en/authorize?client_id=%s&response_type=code&scope=%s&redirect_uri=%s" % (spotipy_client_id, parse.quote_plus(scope), parse.quote_plus(spotipy_redirect_uri)))

@app.route('/playlists', methods = ['POST'])
def generate_playlist():
    body = json.loads(request.data)
    code = body.get('code')
    mood = body.get('mood')
    name = body.get('name')

    if code:
        token = spotify_service.generate_token(code,scope)
        tracks = spotify_service.get_playlist_tracks(token)
        track_data = spotify_service.get_track_data(tracks,token)
        playlist_id = spotify_service.create_playlist(name,tracks,token)

        return flask.jsonify(playlist_id)
    else:
        return redirect("https://accounts.spotify.com/en/authorize?client_id=%s&response_type=code&redirect_uri=%s" % (spotipy_client_id, parse.quote_plus(spotipy_redirect_uri)))

def main():
    app.run(host='0.0.0.0', debug=debug, port=port)


if __name__ == '__main__':
    main()
