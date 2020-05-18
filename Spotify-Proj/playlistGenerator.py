import json
import requests

class PlaylistGenerator:
    def __init__(self, token):
        self.token = token
    #returns list of song recommendations given seeds
    #Improvement: add other potential params
    def getSongRec(self, seed_artists, seed_tracks, limit = 100):
        seed_artists = ','.join(seed_artists) 
        seed_tracks = ','.join(seed_tracks) 
        params = {
            'limit': limit,
            'seed_artists': seed_artists,
            'seed_tracks': seed_tracks
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        r = requests.get('https://api.spotify.com/v1/recommendations', params = params, headers = headers)
        json_data = json.loads(r.text)
        tracklist = []
        for track in range(len(json_data['tracks'])):
           tracklist.append(json_data['tracks'][track]['id'])
        return tracklist
    #return filtered tracklist of songs not in doNotInclue
    def filter(self, tracklist, doNotInclude):
        filtered = []
        for track in tracklist:
            if track in doNotInclude:
                pass
            else:
                filtered.append(track)
        return filtered
    def create(self, username, playlist_name):
        params = {
            'name': playlist_name
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }
        r = requests.post('https://api.spotify.com/v1/users/{}/playlists'.format(username), data = json.dumps(params), headers = headers)
        json_data = json.loads(r.text)
        return json_data['id']
        
