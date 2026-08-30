# generate a list of ids for the albums made by this artist
# only the 10 most recent unfortunately but that's good enough for now, revisit later perhaps
# output needs to be run through pull_playlist for each album to get track ids that
# can be run through pull_data_by_id
def pull_artist(sp, artist_url):
    artist_name = sp.artist(artist_url)["name"]
    # increasing the limit above 10 seems to break the request, Spotify might not like that ig
    artist_albums = sp.artist_albums(artist_url, include_groups = "album,song", limit = 1)
    results = artist_albums["items"]
    # Collect album IDs
    album_ids = []
    for counter, album in enumerate(results):
        album_id = results[counter]["id"]
        album_ids.append(album_id)
    return artist_name, album_ids