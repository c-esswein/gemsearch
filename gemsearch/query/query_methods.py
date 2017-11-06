import numpy as np


def rec_query_tracks_with_user(geCalc, playlist, limit):
    ''' Uses queryIds to predict playlist track with User context.
    '''
    queryIds = playlist['extracted_queries']['simple_first_match'].copy()
    queryIds.append(playlist['userId'])
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def rec_tracks_with_user(geCalc, playlist, limit):
    ''' Uses user context alone to rec tracks (query is not included!).
    '''
    queryIds = [playlist['userId']]
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def rec_query_tracks_with_user_scaled(geCalc, playlist, limit):
    ''' Uses queryIds to predict playlist track with User context.
    '''
    queryIds = playlist['extracted_queries']['simple_first_match']
    queryVecs = [geCalc.get_embedding_for_id(vec) for vec in queryIds]
    
    userVec = np.multiply(geCalc.get_embedding_for_id(playlist['userId']), 0.5).tolist()
    queryVecs.append(userVec)
    
    results = geCalc.query_by_vec(
        queryVecs, 
        typeFilter = ['track'], 
        limit = limit
    )
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
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def rec_first_two_query_tracks_with_user(geCalc, playlist, limit):
    ''' Uses simple queryIds to predict playlist tracks.
    '''
    queryIds = playlist['extracted_queries']['simple_first_two_match'].copy()
    queryIds.append(playlist['userId'])
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def rec_first_two_query_tracks_with_user_scaled(geCalc, playlist, limit):
    ''' Uses simple queryIds to predict playlist tracks.
    '''
    
    queryIds = playlist['extracted_queries']['simple_first_two_match']
    queryVecs = [geCalc.get_embedding_for_id(vec) for vec in queryIds]
    
    userVec = np.multiply(geCalc.get_embedding_for_id(playlist['userId']), 0.5).tolist()
    queryVecs.append(userVec)
    
    results = geCalc.query_by_vec(
        queryVecs, 
        typeFilter = ['track'], 
        limit = limit
    )
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
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def rec_query_tracks_with_boosting(geCalc, playlist, limit):
    ''' Uses simple queryIds to predict playlist tracks.
    '''
    # TODO: implement boosting
    queryIds = playlist['extracted_queries']['simple_first_match']
    results = geCalc.query_by_ids(
        queryIds, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results

def rec_random_tracks(geCalc, playlist, limit):
    ''' Uses random recommender to predict playlist tracks.
    '''    
    results = geCalc.random_query_results(
        typeFilter = ['track'], 
        limit = limit
    )
    return results


# ---- helper methods ----

def query_by_mean_vecs(geCalc, queryIds, limit):
    ''' Query with mean of vectors
    '''
    queryVecs = [geCalc.get_embedding_for_id(vec) for vec in queryIds]
    searchVec = np.mean(queryVecs, axis=0)
    
    results = geCalc.query_by_vec(
        searchVec, 
        typeFilter = ['track'], 
        limit = limit
    )
    return results
