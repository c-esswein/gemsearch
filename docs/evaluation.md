
Interpretate score of playlist evaluator:
- run evaluator
    - with user context
    - without user context
- run random guess
- run user only query
- run popularity rec




# Collaborative filtering evaluation

- take all playlists
- build user - track map
- split training: top 0.8 tracks per user (filter users having n < threshold tracks)

- embed training data

- per user
    - get test * precision@k tracks
    - check precision
- accumulate
