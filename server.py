import os
import bottle

# Heroku config vars
debug = (os.environ.get('DEBUG', 'True') == 'True')
port = os.environ.get('PORT', 8080)
spotipy_client_id = os.environ.get('SPOTIPY_CLIENT_ID')
spotipy_client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
spotipy_redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')

app = bottle.Bottle()


@app.route('/hello/<name>')
def index(name):
    return bottle.template('<b>Hello {{name}}</b>!', name=name)


def main():
    app.run(host='0.0.0.0', debug=debug, port=port)


main()
