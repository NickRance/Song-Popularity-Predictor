import requests, json, logging
import pandas as pd
from pprint import pprint
import pickle

AUTHORIZATION_HEADER_VALUE = 'Basic NDM0YmFiM2VhNmM2NDg2MmI3NmJkYWUwOTA0NmU2Njg6ZjFlZmFhZmM5MjA1NDFiYzkyZGNlMTk2MzBhZjk1NzE='


def saveModel(model, filename):
  pickle.dump(model, open(filename, "wb"))

def loadModel(path):
  return pickle.load(open(path, "rb"))


def getSpotifyInfoForLists(trackList):
  #track = tuple({Song_Name},{Artist})
  output = []
  if type(trackList) is list:
    for track in trackList:
      # print(track)
      try:
        output.append(getSpotifyTrackInfo(song_name = track[0], artist_name = track[1]))
      except (IndexError, KeyError) as err:
        print("Error finding %s -%s" % (track[0], track[1]))
        continue
      #getSpotifyInfo
  elif isinstance(trackList, str):
    output.append(getSpotifyPlaylistInfo(trackList))
  return output

def getSpotifyPlaylistInfo(playlistID):
  output = []
  r = requests.post('https://accounts.spotify.com/api/token', headers = {'Authorization': AUTHORIZATION_HEADER_VALUE}, data= {'grant_type': 'client_credentials'})
  token = 'Bearer {}'.format(r.json()['access_token'])
  headers = {'Authorization': token, "Accept": 'application/json', 'Content-Type': "application/json"}
  
  payload = {}
  
  res = requests.get('https://api.spotify.com/v1/playlists/%s/tracks' % (playlistID), params = payload, headers = headers)
  items = res.json()['items']
  for item in items:
    output.append((item['track']['name'], [x['name'] for x in item['track']['artists']], item['track']['uri']))
  return output

def getSpotifyTrackInfo(song_name = 'africa', artist_name = 'toto', spotifyIds='', req_type = 'track'):
    r = requests.post('https://accounts.spotify.com/api/token', headers = {'Authorization': AUTHORIZATION_HEADER_VALUE}, data= {'grant_type': 'client_credentials'})
    token = 'Bearer {}'.format(r.json()['access_token'])
    headers = {'Authorization': token, "Accept": 'application/json', 'Content-Type': "application/json"}
    
    payload = {"q" : "artist:{} track:{}".format(artist_name, song_name), "type": req_type, "limit": "1"}
    # print(spotifyIds)
    if isinstance(spotifyIds, list):
      payload = {"ids" :(",".join(spotifyIds))}
      # print(payload)
      res = requests.get('https://api.spotify.com/v1/audio-features', params = payload, headers = headers)
      pprint(res.json())
    else:
      res = requests.get('https://api.spotify.com/v1/search', params = payload, headers = headers)
      # print(res.json())
      res = res.json()['tracks']['items'][0]
      year = res['album']['release_date'][:4]
      artist_id = res['artists'][0]['id']
      track_id = res['id']
      track_pop = res['popularity']

      res = requests.get('https://api.spotify.com/v1/audio-analysis/{}'.format(track_id), headers = headers)
      res = res.json()['track']
      duration = res['duration']
      end_fade = res['end_of_fade_in']
      key = res['key']
      key_con = res['key_confidence']
      loud = res['loudness']
      mode = res['mode']
      mode_con = res['mode_confidence']
      start_fade = res['start_of_fade_out']
      temp = res['tempo']
      time_sig = res['time_signature']
      time_sig_con = res['time_signature_confidence']
      
      res = requests.get('https://api.spotify.com/v1/artists/{}'.format(artist_id), headers = headers)
      artist_hot = res.json()['popularity']/100
      
    return pd.to_numeric(pd.Series({'duration': duration, 
                      'key': key,
                    'loudness': loud,
                     'mode': mode,
                     'tempo': temp,
                     'artist_hotttnesss': artist_hot,
                     'end_of_fade_in': end_fade,
                     'start_of_fade_out': start_fade,
                     'mode_confidence': mode_con,
                     'key_confidence': key_con,
                     'time_signature': time_sig,
                     'time_signature_confidence': time_sig_con,
                     'year': year})), track_pop

def matchOrder(incorrectShape, correctShape):
    """
    Train and Predictee need to have column names in the same order
    correctOrder ensures that the Training set and the song that's to be predicted have their columns in the correct order
    """
    return(incorrectShape[correctShape.columns.values])

# spotifyUri = 'spotify:user:123862312:playlist:1JdWDyDMEUlUvl9oWfi4p1'.split(':')[-1]
# ids = ['4JpKVNYnVcJ8tuMKjAj50A','2NRANZE9UCmPAS5XVbXL40','24JygzOLM0EmRQeGtFcIcG']
# getSpotifyTrackInfo(spotifyIds = ids)
# pprint(getSpotifyTrackInfo('rolling in the deep', 'adele'))
# pprint(getSpotifyPlaylistInfo(spotifyUri))