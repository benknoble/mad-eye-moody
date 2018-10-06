import os
import flask
from flask import request, render_template, send_file
import authenticate_user


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
        authenticate_user.authenticate()
        return f'Authorized!'

def main():
    app.run(host='0.0.0.0', debug=debug, port=port)


if __name__ == '__main__':
    main()
