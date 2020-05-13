#DO NOT MAKE PUBLIC
API_BASE = 'https://accounts.spotify.com'
REDIRECT_URI = "http://127.0.0.1:5000/authenticate"
SCOPE = 'playlist-read-private playlist-read-collaborative user-top-read'
CLI_ID = 'a9cbe2388645499ab83dc1cae6ca99d8'
CLI_SEC = '36c83a329b5b409ba995a85067cb92cb'
SHOW_DIALOG = True #make False when deploying
SECRET_KEY = 'this is very secret'

#Pick PICK artists/songs out of top N
PICK = 2 
N = 8