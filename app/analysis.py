#make sure to grab the data from pull_song.py
from .pull_song import run_pull_song

# time for some maths
import numpy as np
import pandas as pd

###USER VARIABLES HERE

exclude_music_keys = False
manual_weighting = True
#weight_array might go here, might not be necessary

######################

def analysis_output(target_song_url : str,
                    playlist_url : str,
                    # exclude_music_keys : bool,
                    # manual_weighting : bool
                    ):

    track_name, playlist_name, id_dict, audios = run_pull_song(target_song_url, playlist_url)

    #use this for custom ordering of features
    feature_list = ["id", "duration_ms", "tempo", "key", "mode", "time_signature", "acousticness",
                    "danceability", "energy", "instrumentalness", "liveness", "loudness",
                    "speechiness", "valence"]

    #left as a reminder, not used currently
    unwanted_list = ["analysis_url", "track_href", "type", "uri"]

    if exclude_music_keys:
        del feature_list[3:6]

    #weighting array
    #need to assign this beforehand or manual_weighting fails since the list indices don't exist yet
    weight_array = np.ones(len(feature_list) - 1)

    #extract and organise target song features
    target_song_feats = [audios[0][key] for key in feature_list[1:]]

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
    target_feats_array = np.array(target_song_feats)
    feat_matrix = np.array(feat_list_list)

    #normalising duration_ms and tempo, indices 0 and 1 since id is no longer present
    #even if the user chooses to exclude key, mode, etc. it shouldn't affect the indexing here since duration
    #and tempo come before those features
    #DO NOT forget to include and normalise target song too
    for index in range(2):
        values = [target_feats_array[index]]
        values.extend([feat_matrix[track][index] for track in range(len(feat_matrix))])
        target_feats_array[index] = (values[0]-min(values))/(max(values)-min(values))
        for track in range(len(values)-1):
            feat_matrix[track][index] = [((x-min(values))/(max(values)-min(values))) for x in values[1:]][track]

    #calculate euclidean distances
    dist_matrix = feat_matrix - target_feats_array
    distances = np.sqrt((weight_array * dist_matrix * dist_matrix).sum(axis = 1))

    #match names with song IDs using id_dict from pull_song.py
    id_dict_dicts = [dic for key, dic in id_dict.items() if isinstance(dic, dict)]
    #don't need the target track to be in the reversed dictionary so index to skip it
    reverse_id_dict = {id_str : name for name, id_str in id_dict_dicts[1].items()}
    assigned_distances = [[reverse_id_dict[id], float(distance)] for id, distance in zip(id_list, distances)]

    #format into a table for easy viewing
    distance_table = pd.DataFrame(assigned_distances, columns = ["Song", "Distance"])
    distance_table_sorted = distance_table.sort_values("Distance")
    #json conversion for export
    distance_table_json = distance_table.to_json()
    distance_table_sorted_json = distance_table_sorted.to_json()
    distance_table_sorted.index = range(1, len(distance_table_sorted) + 1)
    return (track_name, 
            playlist_name,
            distance_table_json,
            distance_table_sorted_json)