import numpy as np
from gemsearch.storage.Storage import Storage


def rec_multiple_queries_tracks_with_user(geCalc, playlist, limit):
    ''' Uses multiple_queries to predict playlist track with User context.
    '''
    queryIds = playlist['extracted_queries']['multiple_queries'].copy()
    queryIds.append(playlist['userId'])
    results = geCalc.query_by_ids(queryIds, typeFilter=['track'], limit=limit)
    return results


def rec_multiple_queries_tracks(geCalc, playlist, limit):
    ''' Uses multiple_queries to predict playlist track.
    '''
    queryIds = playlist['extracted_queries']['multiple_queries'].copy()
    results = geCalc.query_by_ids(queryIds, typeFilter=['track'], limit=limit)
    return results


def rec_album_or_query(geCalc, playlist, limit):
    ''' Uses simple query to check if album is first hit and returns items from db, simple rec tracks
    otherwise.
    '''
    queryId = playlist['extracted_queries']['simple_first_match'][0]

    if queryId.startswith('spotify:album:'):
        # return album tracks
        albumCol = Storage().getCollection('albums')
        albumDb = albumCol.find_one({'uri': queryId})
        if albumDb:
            # transform to result obj
            trackResult = [{'id': trackId} for trackId in albumDb['tracks']]
            return trackResult[:limit]
        else:
            print('album not found, id: ' + str(queryId))

    # else: return simple query by id
    results = geCalc.query_by_ids([queryId], typeFilter=['track'], limit=limit)
    return results


def rec_query_tracks_with_user(geCalc, playlist, limit):
    ''' Uses queryIds to predict playlist track with User context.
    '''
    queryIds = playlist['extracted_queries']['simple_first_match'].copy()
    queryIds.append(playlist['userId'])
    results = geCalc.query_by_ids(queryIds, typeFilter=['track'], limit=limit)
    return results


def rec_tracks_with_user(geCalc, playlist, limit):
    ''' Uses user context alone to rec tracks (query is not included!).
    '''
    queryIds = [playlist['userId']]
    results = geCalc.query_by_ids(queryIds, typeFilter=['track'], limit=limit)
    return results


def rec_query_tracks_with_user_scaled(geCalc, playlist, limit):
    ''' Uses queryIds to predict playlist track with User context.
    '''
    queryIds = playlist['extracted_queries']['simple_first_match']
    queryVecs = [geCalc.get_embedding_for_id(vec) for vec in queryIds]

    userVec = np.multiply(geCalc.get_embedding_for_id(playlist['userId']), 0.5)
    queryVecs.append(userVec)
    queryVec = sum_vecs(queryVecs)

    results = geCalc.query_by_vec(queryVec, typeFilter=['track'], limit=limit)
    return results


def rec_query_tracks_with_user_mean(geCalc, playlist, limit):
    ''' Uses queryIds to predict playlist track with User context. Search vectors are not added
    but average is computed.
    '''
    queryIds = playlist['extracted_queries']['simple_first_match'].copy()
    queryIds.append(playlist['userId'])

    return query_by_mean_vecs(geCalc, queryIds, limit)


def rec_first_two_query_tracks(geCalc, playlist, limit):
    ''' Uses simple queryIds to predict playlist tracks.
    '''
    queryIds = playlist['extracted_queries']['simple_first_two_match']
    results = geCalc.query_by_ids(queryIds, typeFilter=['track'], limit=limit)
    return results


def rec_first_two_query_tracks_with_user(geCalc, playlist, limit):
    ''' Uses simple queryIds to predict playlist tracks.
    '''
    queryIds = playlist['extracted_queries']['simple_first_two_match'].copy()
    queryIds.append(playlist['userId'])
    results = geCalc.query_by_ids(queryIds, typeFilter=['track'], limit=limit)
    return results


def rec_first_two_query_tracks_with_user_scaled(geCalc, playlist, limit):
    ''' Uses simple queryIds to predict playlist tracks.
    '''

    queryIds = playlist['extracted_queries']['simple_first_two_match']
    queryVecs = [geCalc.get_embedding_for_id(vec) for vec in queryIds]

    userVec = np.multiply(geCalc.get_embedding_for_id(playlist['userId']), 0.5)
    queryVecs.append(userVec)

    queryVec = sum_vecs(queryVecs)

    results = geCalc.query_by_vec(queryVec, typeFilter=['track'], limit=limit)
    return results


def rec_first_two_query_tracks_mean(geCalc, playlist, limit):
    ''' Uses queryIds to predict playlist track with User context. Search vectors are not added
    but average is computed.
    '''
    queryIds = playlist['extracted_queries']['simple_first_two_match']

    return query_by_mean_vecs(geCalc, queryIds, limit)


def rec_query_tracks(geCalc, playlist, limit):
    ''' Uses simple queryIds to predict playlist tracks.
    '''
    queryIds = playlist['extracted_queries']['simple_first_match']
    results = geCalc.query_by_ids(queryIds, typeFilter=['track'], limit=limit)
    return results


def rec_query_tracks_with_boosting(geCalc, playlist, limit):
    ''' Uses simple queryIds to predict playlist tracks.
    '''
    # TODO: implement boosting
    queryIds = playlist['extracted_queries']['simple_first_match']
    results = geCalc.query_by_ids(queryIds, typeFilter=['track'], limit=limit)
    return results


def rec_random_tracks(geCalc, playlist, limit):
    ''' Uses random recommender to predict playlist tracks.
    '''
    results = geCalc.random_query_results(typeFilter=['track'], limit=limit)
    return results


# ---- helper methods ----


def query_by_mean_vecs(geCalc, queryIds, limit):
    ''' Query with mean of vectors
    '''
    queryVecs = [geCalc.get_embedding_for_id(vec) for vec in queryIds]
    searchVec = np.mean(queryVecs, axis=0)

    results = geCalc.query_by_vec(searchVec, typeFilter=['track'], limit=limit)
    return results


def sum_vecs(vecs):
    searchVec = None

    for vec in vecs:
        if searchVec is not None:
            searchVec = searchVec + vec
        else:
            searchVec = vec

    return searchVec