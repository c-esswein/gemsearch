from flask import Flask, jsonify, request

from gemsearch.embedding.ge_calc import GeCalc
from gemsearch.query.elastic_search import search as es_search

app = Flask(__name__)

geCalc = GeCalc('data/tmp_test_1/')

@app.route("/api/query")
def query():
    ids = request.args.get('ids')

    if ids is None:
        return jsonify([])        

    idList = ids.split('|')

    try:
        result = geCalc.query_by_ids(idList)
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
    result = es_search(term)
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
    return jsonify({
        'nodes': geCalc.get_graph_data().tolist(),
        'mapping': geCalc.get_lbl_mapping(),
        'graph': geCalc.get_graph().tolist()
    })

@app.route("/api/nodes")
def get_graph_nodes():
    return jsonify({
        'graph': geCalc.get_graph()
    })

if __name__ == "__main__":
    app.run()