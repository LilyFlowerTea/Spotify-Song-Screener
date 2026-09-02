# Spotify-Song-Screener
Software to pull one song from a Spotify account, then find the closes matches in a given playlist based on audio data.

UPDATED
Webpage is working, I plan to have 3+ methods:
1. Rank the songs in a playlist by similarity
2. Rank an artist's songs by similarity
3. Generate recommendations based on the given song, maybe even the average features of a playlist later on?

Current workflow
1. Spotify WebAPI using Spotipy to pull song and playlist data\
2. Some method of fetching audio files using the song names from 1)
3. Use librosa to extract audio features
4. Use NumPy in optimisation to find the songs in playlist with the shortest vector distance from target song
5. Return list
6. Optional - Allow different parameter weightings

Things to look into:
Essentia
librosa