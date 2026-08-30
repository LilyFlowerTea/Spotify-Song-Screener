#pull target playlist
def pull_playlist(sp, id_dict : dict, playlist_url : str):
    if "playlist" in playlist_url:
        target_playlist = sp.playlist(playlist_url)
        playlist_name = target_playlist["name"]
        results = sp.playlist_items(playlist_url)
        # Collect playlist track IDs and names
        for obj in results["items"]:
            track = obj["item"]
            track_id = track["id"]
            id_dict["comparison tracks"][track["name"]] = track_id
            # Line below is no longer necessary, just reverse id_dict to get song names
            # Could be used if I wanted artist name as well
            # name_list.append((track['name'], track['artists'][0]['name']))
    elif "album" in playlist_url:
        target_playlist = sp.album_tracks(playlist_url)
        playlist_name = sp.album(playlist_url)["name"]
        items = target_playlist["items"]
        for count in range(len(items)):
            id_dict["comparison tracks"][items[count]["name"]] = items[count]["id"]
    return playlist_name, id_dict