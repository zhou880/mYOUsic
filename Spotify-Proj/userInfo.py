import json
import requests
import random
class UserInfo:
    def __init__(self, token):
        self.token = token
    #Returns list of 50 playlist ids
    def getPlaylists(self):
        params = {
            'limit': 50,
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        r = requests.get('https://api.spotify.com/v1/me/playlists', params = params, headers = headers)
        json_data = json.loads(r.text)
        playlist_list = []
        for i in range(len(json_data['items'])):
            #print(json_data['items'][i]['name'])
            playlist_list.append(json_data['items'][i]['id'])
        
        return playlist_list

    #Returns dict of songs not to include in suggestions - based off select playlists
    def getSongs(self, playlists):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        doNotInclude = {}
        for playlistNum in range(len(playlists)):
            params = {
                'fields' : 'items(track(id))'
            }
            r = requests.get('https://api.spotify.com/v1/playlists/{}/tracks'.format(playlists[playlistNum]), params = params, headers = headers)
            json_data = json.loads(r.text)

            entirePlaylist = json_data['items']
            for song in entirePlaylist:
                if song['track'] is not None:
                    doNotInclude[song['track']['id']] = 1
        return doNotInclude

    #return pick artists/tracks from top N artists- currently set for medium term (up to 6 months)
    def getTopNArtistsAndTracks(self, pick, N):
        params = {
            'limit': N,
            'time_range': 'medium_term'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        #artist
        r = requests.get('https://api.spotify.com/v1/me/top/{}'.format('artists'), headers = headers, params = params)
        json_data = json.loads(r.text)
        topNArtists = []
        for artist in range(len(json_data['items'])):
            topNArtists.append(json_data['items'][artist]['id'])
        
        #track
        r = requests.get('https://api.spotify.com/v1/me/top/{}'.format('tracks'), headers = headers, params = params)
        json_data = json.loads(r.text)
        topNTracks = []
        for artist in range(len(json_data['items'])):
            topNTracks.append(json_data['items'][artist]['id'])

        pick_artists = random.sample(topNArtists, pick)
        pick_tracks = random.sample(topNTracks, pick)
        return pick_artists, pick_tracks





    #print name of song given id
    def printSongNameFromID(self, id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        r = requests.get('https://api.spotify.com/v1/tracks/{}'.format(id), headers = headers)
        json_data = json.loads(r.text)
        return (json_data['name'])
        
    #print name of artist given id
    def printArtistNameFromID(self, id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        r = requests.get('https://api.spotify.com/v1/artists/{}'.format(id), headers = headers)
        json_data = json.loads(r.text)
        return (json_data['name'])
        
    #print name of playlist given id
    def printPlaylistNameFromID(self, id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        r = requests.get('https://api.spotify.com/v1/playlists/{}'.format(id), headers = headers)
        json_data = json.loads(r.text)
        return (json_data['name'])
        