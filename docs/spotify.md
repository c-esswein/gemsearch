# Spotify Connector overview

Possible User status: [NEW, SPOTIFY_SYNCED, EMBEDDED, PARTIAL_EMBEDDED]

User data in MongoDB:
* hashed username
* status
* created timestamp
* last_sync timestamp

## Login Process on Client

- User requests login
- User auth with Spotify --> token + username is returned
- check Gemsearch API for user --> show status
- if status !== EMBEDDED --> recheck status after fixed interval
- if status is EMBEDDED or PARTIAL_EMBEDDED --> include current user in query

## User API
User check request:
- NEW USER: sync music lib, return missing / known tracks
- EXISTING USER: return status + missing / known tracks

Query:
- check if user context is set + if user is embedded, then include user vertex as query item

## Services

Crawler:
Check for new tracks (every 10sec) in DB, then
- crawl tracks, store data and set gemsearch_status=CRAWLED


Embedder:
Check for new users (every 10min)
- collect new users + tracks
- create embedding
- restart api
- set user status -> embedded
- set track status -> embedded

