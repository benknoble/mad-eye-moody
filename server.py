import os
import flask
from flask import request, render_template, send_file, redirect

# Heroku config vars
debug = (os.environ.get('DEBUG', 'True') == 'True')
port = os.environ.get('PORT', 8080)
spotipy_client_id = os.environ.get('SPOTIPY_CLIENT_ID')
spotipy_client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
spotipy_redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')

app = flask.Flask(__name__)


@app.route('/')
@app.route("/callback")
def index():
    token = request.headers.get('Authorization')
    if token:
        return send_file("index.html")
    else:
        return redirect("https://accounts.spotify.com/en/authorize?client_id=%s&response_type=code&redirect_uri=%s" % (spotipy_client_id, spotipy_redirect_uri))

def main():
    app.run(host='0.0.0.0', debug=debug, port=port)


if __name__ == '__main__':
    main()
