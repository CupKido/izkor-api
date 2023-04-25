from flask import Flask, jsonify, request
import json
from izkor_wrapper import izkor_wrapper
import argparse
app = Flask(__name__)

@app.route('/GetHalalimByName', methods=['GET'])
def get_halalim_by_name():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    if first_name == '' and last_name == '':
        return None, 404
    halalim = izkor_wrapper.get_halalim_by_name(first_name, last_name)
    halalim_jsons = list(map(lambda x: x.__dict__, halalim))
    json_data = json.dumps(halalim_jsons)
    decoded_data = json_data.encode('utf-8').decode('unicode_escape')
    response = app.response_class(
        response=decoded_data,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/GetHalal', methods=['GET'])
def get_halal_by_id():
    id = request.args.get('id')
    if id == '':
        return None, 404
    halal = izkor_wrapper.get_halal_by_id(id)
    json_data = json.dumps(halal.__dict__)
    decoded_data = json_data.encode('utf-8').decode('unicode_escape')
    response = app.response_class(
        response=decoded_data,
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    port = 3500
    parser = argparse.ArgumentParser(description='API server for israeli fallen soldiers')
    parser.add_argument('-p','--port', type=int, help='what port to use')
    args = parser.parse_args()
    if args.port is not None:
        port = args.port
    app.run(port=port, debug=True)
