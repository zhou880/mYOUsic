from flask import Flask, render_template, request, redirect, session, flash
import requests
import json

from userInfo import UserInfo
from playlistGenerator import PlaylistGenerator
from secrets import *

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
        return render_template('index.html')

@app.route("/verify")
def verify():
    auth_url = f'{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    return redirect(auth_url)

@app.route("/authenticate")
def callback():
    session.clear()
    code = request.args.get('code')
    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri":"http://127.0.0.1:5000/authenticate",
        "client_id": CLI_ID,
        "client_secret": CLI_SEC
        })
    res_body = res.json()
    session["toke"] = res_body.get("access_token", None)
    if session["toke"] == None:
        flash('Authentication not successful. Try again!')
        return render_template('index.html')
    else:
        return redirect('/select')

@app.route("/select")
def select():
    return render_template('select.html')

@app.route("/create")
def create():
    token = session['toke']

    user = UserInfo(token)
    playlist_list = user.getPlaylists()
    doNotInclude = user.getSongs(playlist_list)
    topNArtists, topNTracks = user.getTopNArtistsAndTracks(PICK, N)
    #PlaylistGeneration
    playlist = PlaylistGenerator(token)
    tracklist = playlist.getSongRec(topNArtists, topNTracks)
    filtered_songs = playlist.filter(tracklist, doNotInclude)
    filtered_songs = json.dumps(filtered_songs) #format songs for html
    return render_template('create.html', songs=filtered_songs)


if __name__ == '__main__':
    app.run(debug = True)
