from flask import Flask, render_template, request, flash, redirect, session, url_for, abort, jsonify
import requests
import json

from userInfo import UserInfo
from playlistGenerator import PlaylistGenerator
from secrets import *

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    session.clear()
    if request.method == "POST":
        session['username'] = request.form['username']
        return redirect(url_for('verify'))
    return render_template('index.html')

@app.route("/verify")
def verify():
    auth_url = f'{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    return redirect(auth_url)

@app.route("/authenticate")
def callback():
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
        
        return render_template('index.html')
    else:
        return redirect('/select')

@app.route("/select",  methods=['GET', 'POST'])
def select():
    if request.method == "POST":
        playlist_name = request.form['playlist-name']
        session['playlist-name'] = playlist_name
        print("Playlist {} created!".format(playlist_name))
        print("Username is {}".format(session['username']))
        
        try:
            playlistGenerator = PlaylistGenerator(session['toke'])
            session['playlist-id'] = playlistGenerator.create(session['username'], session['playlist-name'])
        except:
            abort(500) #likely a wrong username
        
        return redirect(url_for('create'))

    return render_template('select.html')

@app.route("/create", methods=['GET', 'POST'])
def create():
    try:
        token = session['toke']
        user = UserInfo(token)
        playlist = PlaylistGenerator(token)
        filtered_songs = []
        if request.method == "POST":
            if request.form.get('btn') == 'generate-songs': #Generate new songs option was selected
                #
                playlist_list = user.getPlaylists()
                doNotInclude = user.getSongs(playlist_list)
                topNArtists, topNTracks = user.getTopNArtistsAndTracks(PICK, N)
                
                #PlaylistGeneration
                tracklist = playlist.getSongRec(topNArtists, topNTracks)
                filtered_songs = playlist.filter(tracklist, doNotInclude)
                filtered_songs = json.dumps(filtered_songs) #format songs for html file
            else:
                #Add song option was selected 
                # **Note, ImmutableDict not applicable for the id = "add" form. Used ajax to retrieve song uri information from javascript var and so that page would not refresh
                
                requested_song_uri = request.get_json()["song_id"]
                playlist.addSong(session['playlist-id'], requested_song_uri)
                
    except:
        abort(500)

    return render_template('create.html', songs=filtered_songs)

#Error Handling
@app.errorhandler(500)
def internal_error500(error):
    return render_template('error500.html')

if __name__ == '__main__':
    app.run(debug = True)
