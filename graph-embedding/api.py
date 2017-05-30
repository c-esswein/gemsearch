from flask import Flask, jsonify, request
from ge_calc import GeCalc

app = Flask(__name__)

#geCalc = GeCalc('')
geCalc = GeCalc('graph-embedding/')

@app.route("/api/query")
def query():
    ids = request.args.get('ids')

    if ids is None:
        return jsonify([])        

    idList = ids.split('|')

    try:
        result = geCalc.query_by_ids(idList)
        return jsonify(result)
    except ValueError:
        return jsonify([])

@app.route("/api/object/<id>")
def get_object_id(id):
    result = geCalc.get_item_by_item_id(id)
    if result is not None:
        return jsonify([result])
    else:
        return jsonify([])

if __name__ == "__main__":
    app.run()