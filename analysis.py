


#DON'T forget to import the data from pull_song.py



# time for some maths
import numpy as np

audios = [{'audio_features': [{'acousticness': 0.23, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/1qVQIlH6SyNDzNson7ZRy9', 'danceability': 0.467, 'duration_ms': 212573, 'energy': 0.485, 'id': '1qVQIlH6SyNDzNson7ZRy9', 'instrumentalness': 3.5e-06, 'key': 5, 'liveness': 0.0934, 'loudness': -8.706, 'mode': 1, 'speechiness': 0.035, 'tempo': 83.515, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/1qVQIlH6SyNDzNson7ZRy9', 'type': 'audio_features', 'uri': 'spotify:track:1qVQIlH6SyNDzNson7ZRy9', 'valence': 0.193}, {'acousticness': 0.263, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/6dti5eXjL9FxAZyETT5NEj', 'danceability': 0.607, 'duration_ms': 221973, 'energy': 0.85, 'id': '6dti5eXjL9FxAZyETT5NEj', 'instrumentalness': 0.00578, 'key': 8, 'liveness': 0.144, 'loudness': -5.989, 'mode': 1, 'speechiness': 0.0599, 'tempo': 105.025, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/6dti5eXjL9FxAZyETT5NEj', 'type': 'audio_features', 'uri': 'spotify:track:6dti5eXjL9FxAZyETT5NEj', 'valence': 0.559}, {'acousticness': 0.00241, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/3qdffH7BqUr4kOxaenMkiZ', 'danceability': 0.723, 'duration_ms': 195027, 'energy': 0.761, 'id': '3qdffH7BqUr4kOxaenMkiZ', 'instrumentalness': 9.01e-05, 'key': 6, 'liveness': 0.116, 'loudness': -4.011, 'mode': 1, 'speechiness': 0.0307, 'tempo': 129.999, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/3qdffH7BqUr4kOxaenMkiZ', 'type': 'audio_features', 'uri': 'spotify:track:3qdffH7BqUr4kOxaenMkiZ', 'valence': 0.832}, {'acousticness': 0.00872, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2DEvSP6nGeJJhuAIRGHbaW', 'danceability': 0.808, 'duration_ms': 208747, 'energy': 0.701, 'id': '2DEvSP6nGeJJhuAIRGHbaW', 'instrumentalness': 2.37e-05, 'key': 6, 'liveness': 0.252, 'loudness': -4.638, 'mode': 1, 'speechiness': 0.0331, 'tempo': 123.004, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/2DEvSP6nGeJJhuAIRGHbaW', 'type': 'audio_features', 'uri': 'spotify:track:2DEvSP6nGeJJhuAIRGHbaW', 'valence': 0.927}, {'acousticness': 0.645, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2RFs9C6OfM6MaGBphZi3MB', 'danceability': 0.714, 'duration_ms': 222013, 'energy': 0.651, 'id': '2RFs9C6OfM6MaGBphZi3MB', 'instrumentalness': 2.61e-05, 'key': 2, 'liveness': 0.112, 'loudness': -7.862, 'mode': 0, 'speechiness': 0.0338, 'tempo': 106.973, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/2RFs9C6OfM6MaGBphZi3MB', 'type': 'audio_features', 'uri': 'spotify:track:2RFs9C6OfM6MaGBphZi3MB', 'valence': 0.215}]}, {'audio_features': [{'acousticness': 0.103, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2gYj9lubBorOPIVWsTXugG', 'danceability': 0.68, 'duration_ms': 176973, 'energy': 0.922, 'id': '2gYj9lubBorOPIVWsTXugG', 'instrumentalness': 0.0, 'key': 0, 'liveness': 0.0877, 'loudness': -1.215, 'mode': 1, 'speechiness': 0.121, 'tempo': 125.014, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/2gYj9lubBorOPIVWsTXugG', 'type': 'audio_features', 'uri': 'spotify:track:2gYj9lubBorOPIVWsTXugG', 'valence': 0.799}]}]

audios = {'audio_features': [{'acousticness': 0.23, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/1qVQIlH6SyNDzNson7ZRy9', 'danceability': 0.467, 'duration_ms': 212573, 'energy': 0.485, 'id': '1qVQIlH6SyNDzNson7ZRy9', 'instrumentalness': 3.5e-06, 'key': 5, 'liveness': 0.0934, 'loudness': -8.706, 'mode': 1, 'speechiness': 0.035, 'tempo': 83.515, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/1qVQIlH6SyNDzNson7ZRy9', 'type': 'audio_features', 'uri': 'spotify:track:1qVQIlH6SyNDzNson7ZRy9', 'valence': 0.193}, {'acousticness': 0.263, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/6dti5eXjL9FxAZyETT5NEj', 'danceability': 0.607, 'duration_ms': 221973, 'energy': 0.85, 'id': '6dti5eXjL9FxAZyETT5NEj', 'instrumentalness': 0.00578, 'key': 8, 'liveness': 0.144, 'loudness': -5.989, 'mode': 1, 'speechiness': 0.0599, 'tempo': 105.025, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/6dti5eXjL9FxAZyETT5NEj', 'type': 'audio_features', 'uri': 'spotify:track:6dti5eXjL9FxAZyETT5NEj', 'valence': 0.559}, {'acousticness': 0.645, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2RFs9C6OfM6MaGBphZi3MB', 'danceability': 0.714, 'duration_ms': 222013, 'energy': 0.651, 'id': '2RFs9C6OfM6MaGBphZi3MB', 'instrumentalness': 2.61e-05, 'key': 2, 'liveness': 0.112, 'loudness': -7.862, 'mode': 0, 'speechiness': 0.0338, 'tempo': 106.973, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/2RFs9C6OfM6MaGBphZi3MB', 'type': 'audio_features', 'uri': 'spotify:track:2RFs9C6OfM6MaGBphZi3MB', 'valence': 0.215}, {'acousticness': 0.103, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2gYj9lubBorOPIVWsTXugG', 'danceability': 0.68, 'duration_ms': 176973, 'energy': 0.922, 'id': '2gYj9lubBorOPIVWsTXugG', 'instrumentalness': 0.0, 'key': 0, 'liveness': 0.0877, 'loudness': -1.215, 'mode': 1, 'speechiness': 0.121, 'tempo': 125.014, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/2gYj9lubBorOPIVWsTXugG', 'type': 'audio_features', 'uri': 'spotify:track:2gYj9lubBorOPIVWsTXugG', 'valence': 0.799}, {'acousticness': 0, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/37bZGx53B90Kv0ftpFDbDZ', 'danceability': 0.6, 'duration_ms': 252000, 'energy': 0.84, 'id': '37bZGx53B90Kv0ftpFDbDZ', 'instrumentalness': 0, 'key': 7, 'liveness': 0.09, 'loudness': -3.96, 'mode': 1, 'speechiness': 0.03, 'tempo': 112.99, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/37bZGx53B90Kv0ftpFDbDZ', 'type': 'audio_features', 'uri': 'spotify:track:37bZGx53B90Kv0ftpFDbDZ', 'valence': 0.28}]}

audios = audios['audio_features']

#use this for custom ordering of features
feature_list = ["id", "duration_ms", "key", "mode", "time_signature", "tempo", "acousticness",
                "danceability", "energy", "instrumentalness", "liveness", "loudness",
                "speechiness", "valence"]

#removes items key, mode, time_signature, tempo
exclude_music_keys = True
if exclude_music_keys:
    del feature_list[1:6]
print(feature_list)

#left as a reminder, not used currently
unwanted_list = ["analysis_url", "track_href", "type", "uri"]

#weighting array
weight_array = np.ones(len(feature_list)-1)

#extract and organise target song features
target_id = audios[0]['id']
target_feats = [audios[0][key] for key in feature_list[1:]]

#id_array is separate since NumPy only accepts numbers
id_list = []
#list of lists to convert into matrix
feat_list_list = []

#create list of lists then convert to array
#skip the first audio since it's the target
for track in range(len(audios)-1):
    id_list.append(audios[track+1]['id'])
    reorder_list = [audios[track+1][key] for key in feature_list[1:]]
    feat_list_list.append(reorder_list)
    reorder_list = []

#vectors assemble
target_feats_array = np.array(target_feats)
id_array = np.array(id_list)
feat_matrix = np.array(feat_list_list)
print(target_feats_array)
print(id_array)
print(feat_matrix)

#calculate euclidean distances
dist_matrix = feat_matrix - target_feats_array
result = np.sqrt((weight_array * dist_matrix * dist_matrix).sum(axis = 1))
print(result)
import pandas as pd
table = pd.DataFrame(dist_matrix)
print(table)