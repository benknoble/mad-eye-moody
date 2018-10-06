import os
import bottle

# Heroku config vars
debug = (os.environ['DEBUG'] == 'True')
port = os.environ['PORT']
spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

app = bottle.Bottle()


@app.route('/hello/<name>')
def index(name):
    return bottle.template('<b>Hello {{name}}</b>!', name=name)


def main():
    app.run(debug=debug, port=port)


if __name__ == 'main':
    main()
