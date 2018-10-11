import os
import flask
from flask import request, render_template, send_file, redirect
from urllib import parse
import spotify_service
import json
from spotipy import oauth2

# Heroku config vars
debug = (os.environ.get('DEBUG', 'True') == 'True')
port = os.environ.get('PORT', 8080)
spotipy_client_id = os.environ.get('SPOTIPY_CLIENT_ID')
spotipy_client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
spotipy_redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI', "http://www.madeyemoodify.com")
scope = 'user-library-read,playlist-read-private,playlist-modify-public'

app = flask.Flask(__name__)


@app.route('/create')
@app.route("/callback")
def create():
    token = request.args.get('code')
    if token:
        return send_file("create.html")
    else:
        return redirect("https://accounts.spotify.com/en/authorize?client_id=%s&response_type=code&scope=%s&redirect_uri=%s" % (spotipy_client_id, parse.quote_plus(scope), parse.quote_plus(spotipy_redirect_uri)))

@app.route('/')
def index():
    return send_file("index.html")

@app.route('/playlists', methods = ['POST'])
def generate_playlist():
    body = json.loads(request.data)
    code = body.get('code')
    mood = body.get('mood')
    name = body.get('name')
    if not name:
        name = f'madeyemoody {mood} playlist'
    token = body.get('token')

    if not token:
        token = spotify_service.generate_token(code,scope)

    tracks = spotify_service.get_playlist_tracks(token)
    track_data = spotify_service.get_track_data(tracks,token)
    filtered_tracks_ids = spotify_service.filter_tracks(mood, track_data)
    playlist_id = spotify_service.create_playlist(name,filtered_tracks_ids,token)

    return flask.jsonify(playlist_id=playlist_id, token=token)

def main():
    app.run(host='0.0.0.0', debug=debug, port=port)


if __name__ == '__main__':
    main()

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
