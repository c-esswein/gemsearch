from flask import Flask, jsonify, request
import numpy as np
import itertools
import os.path

from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.query.elastic_search import search as es_search
from gemsearch.api.metadata import resolve_items_meta
from gemsearch.api.graph import Graph

app = Flask(__name__)

# dataFolder = 'data/viz/'
dataFolder = 'data/api_1/'
EMBEDDING_FILE = dataFolder + 'pca.em.npy'
geCalc = GeCalc()
geCalc.load_node2vec_data(dataFolder+'node2vec.em', dataFolder+'types.csv')

@app.route("/api/query")
def query():
    ids = request.args.get('ids')

    if ids is None or ids == '':
        return jsonify({
            'success': True,
            'data': []
        })    

    idList = ids.split('|')

    types = request.args.get('types')
    if types is not None:
        types = types.split('|')

    try:
        result = geCalc.query_by_ids(idList, types)
        return jsonify({
            'success': True,
            'data': resolve_items_meta(result)
        })
    except ValueError as exc:
        return jsonify({
            'success': False,
            'errors': [
                str(exc)
            ]
        })

@app.route("/api/object/<id>")
def get_object_id(id):
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
    try:
        result = es_search(term)
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
        'name': item['_source']['name']
    }, result)
    return jsonify({
        'success': True,
        'data': list(resultItems)
    })

# ------- graph routes -------

# params: types, embedding_file
@app.route("/api/nodes")
def get_graph_data():
    types = request.args.get('types')
    if types is not None:
        types = types.split('|')

    lookup = geCalc.get_lookup()
    typeMapping = [item['type'] for item in lookup]

    embeddingFile = request.args.get('embedding_file')
    if embeddingFile is not None:
        embeddingFile = dataFolder + embeddingFile
    else:
        embeddingFile = EMBEDDING_FILE

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
    print(depth)

    node = geCalc.get_item_by_item_id(nodeId)
    nodes = get_graph_helper().get_neighbors(node['embeddingIndex'], depth)

    items = geCalc.get_items_from_embedding_indices(nodes, types)

    return jsonify({
        'nodes': resolve_items_meta(items)
    })

if __name__ == "__main__":
    app.run()
