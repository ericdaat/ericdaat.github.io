---
layout: post
title: From web radio website to Spotify Playlist
date: 2017-08-16
excerpt:
    This post shows how to scrap a list of songs from the KSHE 95 radio website and upload them to a Spotify playlist using the Spotify Web API. I used Python programming language along with Beautiful Soup for scraping and Flask for deploying the app.
cover: radio.jpg
---

As a big fan of Classic Rock living in France, I am very frustrated by the lack of good classic rock radio we have. I spent four months in St Louis, MO, and I had the chance to listen to [KSHE 95](http://www.kshe95.com/) every day, playing some of my favorite classic rock tunes. Unfortunately, I can't listen to this radio in France as they block it. Fortunately, their website shows the [songs that have been playing earlier](http://player.listenlive.co/20101/en/songhistory). I decided to scrap this page, make myself an empty [Spotify playlist](https://open.spotify.com/user/ericda/playlist/3BCcE8T945z1MnfPWkFsfX), and automatically add in the KSHE tracks.

So far, I am able to:

* Scrap KSHE's web page, and get a list of 10 songs they've played
* Find the songs on Spotify thanks to their web API
* Upload them to a playlist I created, making sure there is no duplicate

My next steps include:

* Automate this with a cron (or use something smarter like [Airflow](https://airflow.incubator.apache.org/)) so the playlist keeps getting updated
* Pull some stats about what's playing, and when, trying to predict the next song, or mood, who knows what ...

Feel free to ping me if you want to help. You can have a look at the code on my [Github repository](https://github.com/ericdaat/kshe-to-spotify).

## Scraping KSHE 95 song history

If you visit [KSHE 95 song history page](http://player.listenlive.co/20101/en/songhistory), you'll find a list of the 10 previously played songs.

![alt](/assets/img/articles/kshe/kshe-song-history.png)

By inspecting the page using your favorite browser, you should see the list of these songs within a Javascript variable.

![alt](/assets/img/articles/kshe/kshe-song-history-source.png)

I am very new to webscraping, but Python libraries like [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) make this really easy and straightforward. I just had to write the following lines to get the song list I wanted.

``` python
from bs4 import BeautifulSoup
import requests
import json
from operator import itemgetter

def get_song_history(player_url):
    soup = BeautifulSoup(requests.get(player_url).text, 'html.parser')
    song_history = soup.find('section', {'id': ['songHistory']})
    song_history_json = json.loads(
        song_history.find('script').text.split(';')[0].split('var songs = ')[-1]
    )
    song_history_json.sort(key=itemgetter('timestamp'))

    return song_history_json

song_history = get_song_history('http://player.listenlive.co/20101/en/songhistory')
```

This would return a json that looks like the following.

``` json
[
  {
    "artist": "JOURNEY",
    "timestamp": 1502900650000,
    "title": "LOVIN',TOUCHIN'/CITY OF THE ANGELS"
  },
  {
    "artist": "DOORS",
    "timestamp": 1502901058000,
    "title": "BREAK ON THROUGH"
  },
  {
    "artist": "VAN HALEN",
    "timestamp": 1502901792000,
    "title": "JUMP"
  },
  {
    "artist": "JOE WALSH",
    "timestamp": 1502902038000,
    "title": "LIFE'S BEEN GOOD"
  },
  {
    "artist": "SOUNDGARDEN",
    "timestamp": 1502902593000,
    "title": "SPOONMAN"
  },
  {
    "artist": "STYX",
    "timestamp": 1502903312000,
    "title": "COME SAIL AWAY"
  },
  {
    "artist": "CHEAP TRICK",
    "timestamp": 1502903798000,
    "title": "LONG TIME COMING"
  },
  {
    "artist": "DEF LEPPARD",
    "timestamp": 1502903995000,
    "title": "BRINGIN' ON THE HEARTBREAK"
  },
  {
    "artist": "BLACK SABBATH",
    "timestamp": 1502904272000,
    "title": "PARANOID"
  },
  {
    "artist": "MONTROSE",
    "timestamp": 1502904437000,
    "title": "ROCK CANDY"
  }
]
```

## Uploading the songs to a Spotify Playlist

During this part, we are going to use the [Spotify Web API](https://developer.spotify.com/web-api/). I found the API very straightforward and easy to deal with. The documentation is clear and they show a lot of examples that help. You will need to setup a Developer account and register an Application. This will provide you credentials that you will need for the rest of this post.

### Authorization

I had some trouble figuring this part at first, but it's not that big of a deal once you understand the logic behind it. The [Spotify documentation](https://developer.spotify.com/web-api/authorization-guide/) explains it really well, but I will do a little recap here. There is basically three ways you can authenticate, which will give you an access token you will send within your HTTP requests. I only tried two out of three:

* Authorization Code Flow: will give you a user access token that will enable you to retrieve some personal informations, as well as modifying your playlists, library, etc ...
* Client Credentials: will only let you retrieve public informations about artists, tracks, albums, but nothing involving user's data.

For our purpose, we will need *Authorization Code Flow* because we want to modify our own playlist. Let's see how we do this. The following picture taken from Spotify documentation explains it well how the authorization code flow works.

![alt](/assets/img/articles/kshe/spotify-auth.png)

What happens is:

* We need a web application (can run on *localhost*) from where we will send an authentication request, using a simple HTTP *GET* method along with some credentials and a *redirect-uri* (our web application's url).
* Spotify will prompt the user to login, and will redirect to the *redirect-uri* we passed along with an *authorization-code* within the request.
* We exchange this code we received to a token using an HTTP *POST* request.
* From now on, we can use the Spotify API with this token we stored. It will be valid for 3600 seconds and can be refreshed when needed.

To do this, I used the two functions below within a Flask application.

``` python
def _authorization_code_flow_authentication(self):
    """ Builds the URL to redirect to in order to show the login form
    Returns a URL string
    """
    return 'https://accounts.spotify.com/authorize?{0}'.format(
        urlencode({
            'client_id': self._client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'playlist-modify-public playlist-modify-private',
            'show_dialog': False
        }))

def _client_credentials_authentication(self, authorization_code, redirect_uri):
    """ Exhanges an authorization code to an access token
    Returns a json response containing the token along with other informations
    """
    auth_header = base64.b64encode(
        '{0}:{1}'.format(self._client_id, self._client_secret)
    ).encode('ascii')

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers={'Authorization': 'Basic {0}'.format(auth_header.decode('ascii'))},
        data={
            'grant_type':'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'scope': 'playlist-modify-public playlist-modify-private'
        })

    return response.json()
```

And the Flask app code is the following:

``` python
@app.route('/auth')
def auth():
    """ Redirects to the Spotify login form
    """
    return redirect(api._authorization_code_flow_authentication())


@app.route('/callback')
def callback():
    """ Called by the Spotify API if login is succesful, exchanges
    authorization code in favor of an access token.
    Returns a json response containing the access token so
    we can store it within our application.
    """
    response = api._client_credentials_authentication(
            request.args['code'],
            api.redirect_uri)

    api._access_token = response["access_token"]
    token_type = response["token_type"]
    api._token_expires_in = response["expires_in"]

    logging.info('authenticated')

    return jsonify(
            authenticated=True,
            token_type=token_type,
            token_expires_in=api._token_expires_in
        )
```

My Flask application runs on ```localhost:9999```. When I registered my Spotify Application, I specified the *redirect-uri* to be ```http://localhost:9999/callback```. I start the authentication process by doing a *GET* request on ```localhost:9999/auth``` (I know, a *POST* would be cleaner) which redirects to the Spotify login form that then redirects back to ```localhost:9999/callback``` with the *authorization-code* so I can send the last request to exchange the *authorization-code*in favor of the token (phew!).

Note: The few lines code I showed above is just a snippet that won't work as is since I am using classes and all. Please have a look [here](https://github.com/ericdaat/kshe-to-spotify/blob/master/flask-server/application/spotify_api.py) for the full Spotify API code, and [here](https://github.com/ericdaat/kshe-to-spotify/blob/master/flask-server/application/app.py) for the full Flask API code.

### Searching for songs

Now that we are authenticated, let's have some fun with the Spotify Web API.

Since we have the list of tracks we scraped from KSHE 95 website as a JSON, Python will use it as a list of dict. From this list, we can just iterate over each dict that contains the song name and artist and search for the song using Spotify API. We will be able to retrieve a lot of informations on the track, artist, album, etc ... We do this with the following function.

``` python

def search_track(self, track_name, artist_name, limit=1):
    """ Searches for a song given its title and artist name
    Returns a dict containing informations on the song
    """

    try:
        response = requests.get(
            'https://api.spotify.com/v1/search',
            params={
                'q':'artist:"{0}"%20track:"{1}"'.format(artist_name, track_name),
                'type':'track',
                'limit': limit
            },
            headers={'Authorization': 'Bearer {0}'.format(self._access_token)}
        ).json()['tracks']['items'][0]
    except:
        logging.warning(
            'could not find track {0} from {1}'.format(
                track_name,
                artist_name
            )
        )
        return {}

    return {
        'song_name': response['name'],
        'artist_name': response['artists'][0]['name'],
        'album_name': response['album']['name'],
        'popularity': response['popularity'],
        'duration_ms': response['duration_ms'],
        'explicit': response['explicit'],
        'spotify_uri': response['uri'],
        'album_image': response['album']['images'][0]['url']
    }
```

### Adding songs to playlist

Now we simply take all the *spotify_uri* fields from the previous json, and call the following function that will update the playlist with our new songs. Note that this won't ignore duplicates. To do so, we will need to manually filter out the tracks that are already existing within the playlist.

``` python

def add_tracks_to_playlist(self, track_uris, playlist_uri):
    """ Adds tracks to a playlist given a list of track uris and a playlist uri
    Returns a JSON response
    """

    return requests.post(
            'https://api.spotify.com/v1/users/{0}/playlists/{1}/tracks'.format(
            self._user_id,
            playlist_uri),
        headers={'Authorization': 'Bearer {0}'.format(self._access_token)},
        data=json.dumps({'uris': track_uris})
    ).json()
```

And that's about it ! You can have a look at my Github repository for the full code. My playlist is public and available on Spotify [here](https://open.spotify.com/user/ericda/playlist/3BCcE8T945z1MnfPWkFsfX). Note that my application is not running on its own yet, which means the playlist is not uploaded regularly. I will look at it as soon as I can find some time. Meanwhile feel free to let me know if this was useful, or don't hesitate to ping me on Github if you want to help !

![alt](/assets/img/articles/kshe/kshe-spotify-playlist.png)
