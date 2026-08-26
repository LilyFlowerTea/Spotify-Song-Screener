#make sure to grab the data from pull_song.py
import pull_song

import pandas as pd

# time for some maths
import numpy as np

audios = pull_song.audios

#use this for custom ordering of features
feature_list = ["id", "duration_ms", "tempo", "key", "mode", "time_signature", "acousticness",
                "danceability", "energy", "instrumentalness", "liveness", "loudness",
                "speechiness", "valence"]

def user_inputs(question, error_msg):
    boolean = input(question).lower()
    while boolean not in ["true", "yes", "false", "no"]:
        boolean = input(error_msg).lower()
    if boolean in ["true", "yes"]:
        return True
    else:
        return False

exclude_music_keys = user_inputs("Would you like to EXCLUDE musical data such as key and time signature? "
                           "These do not contribute significantly to song similarity (Yes/No): ",
               "Error. Would you like to EXCLUDE musical data such as key and time signature? (Yes/No) ")
if exclude_music_keys:
    del feature_list[3:6]
print(f"Exclude musical data such as key and time signature: {exclude_music_keys}")

#old way of getting input, made it modular when I started using weightings
#removes items key, mode, time_signature, tempo
# exclude_music_keys = input("Would you like to EXCLUDE musical data such as key and time signature? "
#                            "These do not contribute significantly to song similarity (Yes/No): ").lower()
# while exclude_music_keys not in ["true", "yes", "false", "no"]:
#     exclude_music_keys = input("Error. Would you like to EXCLUDE musical data such as key and time signature? (Yes/No) ").lower()
# if exclude_music_keys in ["true", "yes"]:
#     del feature_list[3:6]
# print(f"Exclude musical data such as key and time signature: {exclude_music_keys}")

#left as a reminder, not used currently
unwanted_list = ["analysis_url", "track_href", "type", "uri"]

#weighting array
weight_array = np.ones(len(feature_list)-1)
manual_weighting = user_inputs("Would you like to manually set the parameter weightings "
                               "for song characteristics? This will allow for better customisation (Yes/No): ",
                               "Error. Would you like to manually set the parameter weightings for song "
                               "characteristics? (Yes/No) ")
if manual_weighting:
    for feature in range(len(feature_list)-1):
        weight_array[feature] =input(f"Please enter the weight to set for {feature_list[feature+1]}")
    print(f"Your weight array")

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
distance_table = pd.DataFrame(assigned_distances, columns = ["Song", "Distance"])

print(f'Weighted Euclidean distances of songs in the playlist "{pull_song.playlist_name}" '
      f'from "{pull_song.track_name}" are:\n{distance_table.to_string(index = False)}')
distance_table_sorted = distance_table.sort_values("Distance")
distance_table_sorted.index = range(1, len(distance_table_sorted) + 1)
print(f'The closest song matches to "{pull_song.track_name}" in "{pull_song.playlist_name}" '
      f'are:\n{distance_table_sorted.head(10)}')