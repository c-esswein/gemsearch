


# Audio Features
Spotify Audio Features:
https://developer.spotify.com/web-api/get-audio-features/

# Embedding
- Graph has to be fully connected!! and sorted (in file)!?



Online learning:
https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/online_w2v_tutorial.ipynb


# Dim reducing

most algorithms do not perform well on big datasets!

# Tag Cleaning
- remove "-" at beginning and end of string
- trim name
- remove empty ones



# Spotify Connect

Possible User status: [NEW, SPOTIFY_SYNCED, EMBEDDED, PARTIAL_EMBEDDED]
User:
    - hashed username
    - status
    - created timestamp
    - last_sync timestamp

## Processes

Client:
- User auth with spotify --> token + username
- check API for user --> show status

- include current user in query!

API:
    User check:
    - NEW USER: sync music lib, return missing / known tracks
    - EXISTING USER: return status + missing / known tracks

    Query:
    - check if user context is set + if user is embedded

Crawler:
    Check for new tracks (every 10sec)
    - crawl tracks

Embedder:
    Check for new users (every 10min)
    - collect new users + tracks
    - create embedding
    - restart api
    - set user status -> embedded

    Relearn complete model (every x days / users)
