from flask import Flask, jsonify, request
from izkor_wrapper import izkor_wrapper
app = Flask(__name__)

@app.route('/GetHalalimByName', methods=['GET'])
def get_halalim_by_name():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    halalim = izkor_wrapper.get_halalim_by_name(first_name, last_name)
    halalim_jsons = list(map(lambda x: x.get_dict(), halalim))
    return jsonify(halalim_jsons), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/GetHalal', methods=['GET'])
def get_halal_by_id():
    id = request.args.get('id')
    if id == '':
        return None, 404
    halal = izkor_wrapper.get_halal_by_id(id)

if __name__ == '__main__':
    app.run(port=3500, debug=True)
