from gemsearch.utils.logging import getLogger
logger = getLogger(__name__)
from flask import Flask, jsonify, request, make_response
import numpy as np
import itertools
import os.path
import os

from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.query.elastic_search import suggest as es_suggest
from gemsearch.api.metadata import resolve_items_meta
from gemsearch.api.graph import Graph
from gemsearch.api.positions import calc_viz_data, cluster_items
import gemsearch.api.user as userApi
from gemsearch.settings import GEMSEARCH_API_KEY

# ---------- config ----------
dataFolder = os.environ.get('GEMSEARCH_API_FOLDER', 'data/api/')
VIZ_EMBEDDING_FILE = dataFolder + 'pca.em.npy'


# ---------- init ----------
app = Flask(__name__)
geCalc = None
vizGeCalc = None

def initializeApi():
    global geCalc
    global vizGeCalc
    global _graphHelper
    
    # reset weighted graph helper
    _graphHelper = None
    
    print('initialize geCalc')
    geCalc = GeCalc()
    geCalc.load_node2vec_data(dataFolder+'embedding.em', dataFolder+'types.csv')

    print('initialize graph geCalc')
    vizGeCalc = GeCalc()
    vizGeCalc.lookup = geCalc.lookup
    vizGeCalc.embedding = np.load(VIZ_EMBEDDING_FILE)
    print('initialize geCalc finished')

# ---------- / init ----------

@app.route("/api/reload_embedding")
def reloadEmbedding():
    ''' Reloads embedding.
    '''
    token = request.args.get('token')
    if not token == GEMSEARCH_API_KEY:
        return make_response(jsonify({
            'success': False,
            'errors': [
                'Invalid api token'
            ]
        }), 400)

    
    initializeApi()

    return jsonify({
        'success': True,
        'data': []
    })  

@app.route("/api/query")
def query():
    ''' Query for items with multiple object ids.
    '''
    ids = request.args.get('ids')

    # no ids in query
    if ids is None or ids == '':
        return jsonify({
            'success': True,
            'data': []
        })    
    idList = ids.split('|')

    # type filter
    types = request.args.get('types')
    if types is not None:
        types = types.split('|')

    # limit + offset
    limit = request.args.get('limit') or 20
    limit = int(limit)
    offset = request.args.get('offset') or 0
    offset = int(offset)

    # user context
    userContext = request.args.get('user')
    if userContext is not None and userContext != 'undefined':
        idList.append(userContext)

    try:
        result = geCalc.query_by_ids(idList, types, limit, offset)
        resolvedItems = resolve_items_meta(result)

        return jsonify({
            'success': True,
            'data': resolvedItems
        })
    except ValueError as exc:
        logger.error('query error', exc_info=True)        
        return jsonify({
            'success': False,
            'errors': [
                str(exc)
            ]
        })

@app.route("/api/query_viz")
def queryViz():
    ''' Query for items with multiple object ids. Results includes positions and
    items are clustered.
    '''
    ids = request.args.get('ids')

    # no ids in query
    if ids is None or ids == '':
        return jsonify({
            'success': True,
            'data': []
        })    
    idList = ids.split('|')

    # type filter
    types = request.args.get('types')
    if types is not None:
        types = types.split('|')

    # limit + offset
    limit = request.args.get('limit') or 20
    limit = int(limit)    
    offset = request.args.get('offset') or 0
    offset = int(offset)

    # user context
    userContext = request.args.get('user')
    if userContext is not None and userContext != 'undefined':
        idList.append(userContext)

    # cluster distance
    minClusterDistance = request.args.get('minClusterDistance') or 0.05
    minClusterDistance = float(minClusterDistance)

    try:
        # using own embedding calc for graph --> positions are too different...
        result = vizGeCalc.query_by_ids(idList, types, limit, offset)
        resolvedItems = resolve_items_meta(result)

        # append 3D positions
        vizItems = calc_viz_data(resolvedItems, vizGeCalc.embedding)
        clusteredResult, boundingBox = cluster_items(vizItems, minClusterDistance)

        return jsonify({
            'success': True,
            'clusters': clusteredResult,
            'boundingBox': boundingBox.tolist()
        })
    except Exception as exc:
        logger.error('query viz error', exc_info=True)
        return jsonify({
            'success': False,
            'errors': [
                str(exc)
            ]
        })

@app.route("/api/items_near_viz")
def itemsNearViz():
    ''' Query for items which are near given vec. Results includes positions and
    items are clustered.
    '''
    vecStr = request.args.get('vec')
    # no vec in query
    if vecStr is None or vecStr == '':
        return jsonify({
            'success': True,
            'data': []
        })    
    vec = np.array(vecStr.split(','))

    # type filter
    types = request.args.get('types')
    if types is not None:
        types = types.split('|')

    limit = request.args.get('limit') or 20
    limit = int(limit)

    offset = request.args.get('offset') or 0
    offset = int(offset)

    minClusterDistance = request.args.get('minClusterDistance') or 0.05
    minClusterDistance = float(minClusterDistance)

    try:
        # using own embedding calc for graph --> positions are too different...
        result = vizGeCalc.query_by_vec(vec, types, limit, offset)
        resolvedItems = resolve_items_meta(result)

        # append 3D positions
        vizItems = calc_viz_data(resolvedItems, vizGeCalc.embedding)
        clusteredResult, boundingBox = cluster_items(vizItems, minClusterDistance)

        return jsonify({
            'success': True,
            'clusters': clusteredResult,
            'boundingBox': boundingBox.tolist()
        })
    except ValueError as exc:
        logger.error('query viz error', exc_info=True)
        return jsonify({
            'success': False,
            'errors': [
                str(exc)
            ]
        })

@app.route("/api/object/<id>")
def get_object_id(id):
    ''' Get meta data for given object.
    '''
    result = geCalc.get_item_by_item_id(id)
    if result is not None:
        return jsonify({
            'success': True,
            'data': resolve_items_meta([result])
        })
    else:
        return jsonify({
            'success': True,
            'data': []
        })

@app.route("/api/suggest/<term>")
def suggest_item(term):
    ''' Get autocomplete suggestions for given term.
    '''
    try:
        result = es_suggest(term)
    except Exception as exc:
        return jsonify({
            'success': False,
            'errors': [
                str(exc)
            ]
        })

    resultItems = map(lambda item: {
        'id': item['_source']['id'],
        'type': item['_source']['type'],
        'name': item['_source']['name'],
        'highlightName': item['highlight']['name'][0]
    }, result)

    return jsonify({
        'success': True,
        'data': resolve_items_meta(resultItems)
    })


@app.route("/api/recommendations")
def recommendations():
    ''' Return recommendations for given user.
    '''

    # type filter
    types = request.args.get('types')
    if types is not None:
        types = types.split('|')

    # limit + offset
    limit = request.args.get('limit') or 20
    limit = int(limit)
    offset = request.args.get('offset') or 0
    offset = int(offset)

    # user context
    userContext = request.args.get('user')
    if userContext is None or userContext == 'undefined':
        return jsonify({
            'success': False,
            'errors': [
                'User is not set'
            ]
        })

    try:
        # loader user training tracks
        skipIds = []
        if 'track' in types:
            # IMPROVE: also skip artists
            user = userApi.getUser(userContext)
            skipIds = [track['track_uri'] for track in user['tracks']]

        result = geCalc.query_by_ids([userContext], types, limit, offset, skipIds)
        resolvedItems = resolve_items_meta(result)

        return jsonify({
            'success': True,
            'data': resolvedItems
        })
    except ValueError as exc:
        logger.error('query error', exc_info=True)        
        return jsonify({
            'success': False,
            'errors': [
                str(exc)
            ]
        })


# ------- user routes -------

@app.route("/api/user/check/<userName>")
def check_user(userName):
    ''' Checks if user is allready in db.
    '''
    user = userApi.getUser(userName)

    if user is None:
        return jsonify({
            'success': True,
            'data': None
        })
    else:
        missingTrackCount = userApi.getMissingTracks(userName)

        return jsonify({
            'success': True,
            'data': {
                'userName': userName,
                'userStatus': user['userStatus'],
                'latest_sync': user['latest_sync'],
                'syncedTracks': len(user['tracks']),
                'missingTrackCount': missingTrackCount
            }
        })

@app.route("/api/user/sync", methods=['POST'])
def sync_user():
    ''' Sync user spotify data.
    '''
    token = request.form['token']
    userName = request.form['userName']

    if token is None:
        return make_response(jsonify({
            'success': False,
            'errors': [
                'Token is missing'
            ]
        }), 400)

    try:
        # sync music
        syncedTracks, missingTrackCount = userApi.syncUserMusic(userName, token)
        user = userApi.getUser(userName)    

        return jsonify({
            'success': True,
            'data': {
                'userName': userName,
                'userStatus': user['userStatus'],
                'latest_sync': user['latest_sync'],
                'syncedTracks': len(user['tracks']),
                'missingTrackCount': missingTrackCount
            }
        })
    except Exception as exc:
        logger.error('query error', exc_info=True)        
        return jsonify({
            'success': False,
            'errors': [
                str(exc)
            ]
        })


# ------- graph routes -------

# params: types, VIZ_EMBEDDING_FILE
@app.route("/api/nodes")
def get_graph_data():
    types = request.args.get('types')
    if types is not None:
        types = types.split('|')

    lookup = geCalc.get_lookup()
    typeMapping = [item['type'] for item in lookup]

    embeddingFile = request.args.get('VIZ_EMBEDDING_FILE')
    if embeddingFile is not None:
        embeddingFile = dataFolder + embeddingFile
    else:
        embeddingFile = VIZ_EMBEDDING_FILE

    if not os.path.isfile(embeddingFile):
        return jsonify({
            'success': False,
            'errors': [
                'viz embedding file not found'
            ]
        })

    # load embedding
    embedding = np.load(embeddingFile)

    # flatten array to faster loading in client
    flattenEmbedding = embedding.flatten().tolist()

    # embedding = geCalc.get_graph_embedding(types).tolist()

    return jsonify({
        'nodes': flattenEmbedding,
        'typeMapping': typeMapping,
    })

_graphHelper = None

def get_graph_helper():
    '''lazy loader for graph helper.
    '''
    global _graphHelper
    if _graphHelper is None:

        # remove features from graph
        lookup = geCalc.get_lookup()
        def typeRestrictor(nodeId):
            item = lookup[nodeId]
            return item['type'] != 'feature' and item['type'] != 'tag'
            
        _graphHelper = Graph()
        _graphHelper.load_from_edge_list(dataFolder + 'graph_w.txt', typeRestrictor)
    
    return _graphHelper

@app.route("/api/graph")
def get_graph_nodes():
    edges = get_graph_helper().get_edges()
    return jsonify({
        # flatten array
        'edges': list(itertools.chain.from_iterable(edges))
    })

@app.route("/api/neighbors/<nodeId>")
def get_graph_neighbors(nodeId):
    types = request.args.get('types')
    if types is not None:
        types = types.split('|')
    
    depth = int(request.args.get('depth') or 1)

    node = geCalc.get_item_by_item_id(nodeId)
    nodes = get_graph_helper().get_neighbors(node['embeddingIndex'], depth)

    items = geCalc.get_items_from_embedding_indices(nodes, types)

    return jsonify({
        'success': True,
        'nodes': resolve_items_meta(items)
    })


# ----------------- startup -----------------
initializeApi()

if __name__ == "__main__":
    app.run()