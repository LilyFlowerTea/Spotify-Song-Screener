# Spotify-Song-Screener
Software to pull one song from a Spotify account, then find the closes matches in a given playlist based on audio data.

Current workflow
1. Spotify WebAPI using Spotipy to pull song and playlist data
   2. Halfway done 0042, 12/8/26
2. Some method of fetching audio files using the song names from 1)
3. Use librosa to extract audio features
4. Use NumPy in optimisation to find the songs in playlist with the shortest vector distance from target song
5. Return list
6. Optional - Allow different parameter weightings