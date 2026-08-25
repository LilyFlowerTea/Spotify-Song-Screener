


#DON'T forget to import the data from pull_song.py

import pull_song

# time for some maths
import numpy as np

audios = [{'acousticness': 0.23, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/1qVQIlH6SyNDzNson7ZRy9', 'danceability': 0.467, 'duration_ms': 212573, 'energy': 0.485, 'id': '1qVQIlH6SyNDzNson7ZRy9', 'instrumentalness': 3.5e-06, 'key': 5, 'liveness': 0.0934, 'loudness': -8.706, 'mode': 1, 'speechiness': 0.035, 'tempo': 83.515, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/1qVQIlH6SyNDzNson7ZRy9', 'type': 'audio_features', 'uri': 'spotify:track:1qVQIlH6SyNDzNson7ZRy9', 'valence': 0.193}, {'acousticness': 0.263, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/6dti5eXjL9FxAZyETT5NEj', 'danceability': 0.607, 'duration_ms': 221973, 'energy': 0.85, 'id': '6dti5eXjL9FxAZyETT5NEj', 'instrumentalness': 0.00578, 'key': 8, 'liveness': 0.144, 'loudness': -5.989, 'mode': 1, 'speechiness': 0.0599, 'tempo': 105.025, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/6dti5eXjL9FxAZyETT5NEj', 'type': 'audio_features', 'uri': 'spotify:track:6dti5eXjL9FxAZyETT5NEj', 'valence': 0.559}, {'acousticness': 0.645, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2RFs9C6OfM6MaGBphZi3MB', 'danceability': 0.714, 'duration_ms': 222013, 'energy': 0.651, 'id': '2RFs9C6OfM6MaGBphZi3MB', 'instrumentalness': 2.61e-05, 'key': 2, 'liveness': 0.112, 'loudness': -7.862, 'mode': 0, 'speechiness': 0.0338, 'tempo': 106.973, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/2RFs9C6OfM6MaGBphZi3MB', 'type': 'audio_features', 'uri': 'spotify:track:2RFs9C6OfM6MaGBphZi3MB', 'valence': 0.215}, {'acousticness': 0.103, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2gYj9lubBorOPIVWsTXugG', 'danceability': 0.68, 'duration_ms': 176973, 'energy': 0.922, 'id': '2gYj9lubBorOPIVWsTXugG', 'instrumentalness': 0.0, 'key': 0, 'liveness': 0.0877, 'loudness': -1.215, 'mode': 1, 'speechiness': 0.121, 'tempo': 125.014, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/2gYj9lubBorOPIVWsTXugG', 'type': 'audio_features', 'uri': 'spotify:track:2gYj9lubBorOPIVWsTXugG', 'valence': 0.799}, {'acousticness': 0.0, 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/37bZGx53B90Kv0ftpFDbDZ', 'danceability': 0.6, 'duration_ms': 252000, 'energy': 0.84, 'id': '37bZGx53B90Kv0ftpFDbDZ', 'instrumentalness': 0.0, 'key': 7, 'liveness': 0.09, 'loudness': -3.96, 'mode': 1, 'speechiness': 0.03, 'tempo': 112.99, 'time_signature': 4, 'track_href': 'https://api.spotify.com/v1/tracks/37bZGx53B90Kv0ftpFDbDZ', 'type': 'audio_features', 'uri': 'spotify:track:37bZGx53B90Kv0ftpFDbDZ', 'valence': 0.28}]

#use this for custom ordering of features
feature_list = ["id", "duration_ms", "tempo", "key", "mode", "time_signature", "acousticness",
                "danceability", "energy", "instrumentalness", "liveness", "loudness",
                "speechiness", "valence"]

#removes items key, mode, time_signature, tempo
exclude_music_keys = input("Would you like to EXCLUDE musical data such as key and time signature? "
                           "These do not contribute significantly to song similarity: ").lower()
while exclude_music_keys not in ["true", "yes", "false", "no"]:
    exclude_music_keys = input("Error. Would you like to EXCLUDE musical data such as key and time signature? ").lower()
if exclude_music_keys in ["true", "yes"]:
    del feature_list[3:6]
print(f"Exclude musical data such as key and time signature: {exclude_music_keys}")

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
feat_matrix = np.array(feat_list_list)
# print(target_feats_array)
# print(id_array)
# print(f"feat_matrix is {feat_matrix}")

#normalising duration_ms and tempo, indices 0 and 1 since id is no longer present
#DO NOT forget to include and normalise target song too
for index in range(2):
    values = [target_feats_array[index]]
    values.extend([feat_matrix[track][index] for track in range(len(feat_matrix))])
    target_feats_array[index] = (values[0]-min(values))/(max(values)-min(values))
    for track in range(len(values)-1):
        feat_matrix[track][index] = [((x-min(values))/(max(values)-min(values))) for x in values[1:]][track]

#calculate euclidean distances
dist_matrix = feat_matrix - target_feats_array
result = np.sqrt((weight_array * dist_matrix * dist_matrix).sum(axis = 1))

#match names with song IDs using id_dict from pull_song.py
reverse_id_dict = {id_str : name for name, id_str in pull_song.id_dict.items()}
assigned_distances = [[reverse_id_dict[id], float(distance)] for id, distance in zip(id_list, result)]

#format into a table for easy viewing
import pandas as pd
distance_table = pd.DataFrame(assigned_distances, columns = ["Song", "Distance"])

print(f'Weighted Euclidean distances of songs in the playlist "{pull_song.playlist_name}" '
      f'from "{pull_song.track_name}" are:\n{distance_table.to_string(index = False)}')
distance_table_sorted = distance_table.sort_values("Distance")
distance_table_sorted.index = range(1, len(distance_table_sorted) + 1)
print(f'The closest song matches to "{pull_song.track_name}" in "{pull_song.playlist_name}" '
      f'are:\n{distance_table_sorted.head(10)}')