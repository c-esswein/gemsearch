from flask import Flask, jsonify, request

from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.query.elastic_search import search as es_search

app = Flask(__name__)

dataFolder = 'data/graph_10/'
geCalc = GeCalc()
geCalc.load_node2vec_data(dataFolder+'embedding.em', dataFolder+'types.csv')

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
            'data': result
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
            'data': [result]
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
        'id': item['_id'],
        'type': item['_type'],
        'name': item['_source']['name']
    }, result)
    return jsonify({
        'success': True,
        'data': list(resultItems)
    })

# ------- graph routes -------

@app.route("/api/graph")
def get_graph_data():
    types = request.args.get('types')
    if types is not None:
        types = types.split('|')

    return jsonify({
        'nodes': geCalc.get_graph_embedding(types).tolist(),
        # 'mapping': geCalc.get_lbl_mapping(),
        # 'graph': geCalc.get_graph().tolist()
    })

@app.route("/api/nodes")
def get_graph_nodes():
    return jsonify({
        'graph': geCalc.get_graph()
    })

if __name__ == "__main__":
    app.run()