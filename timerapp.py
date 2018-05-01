"""App for testing raw API, to be  merged with orange rabbits"""

from flask import Flask, request, jsonify, abort, make_response

app = Flask(__name__)

timerdata = []

@app.route('/')
def index():
    return "<b>test</b>"

@app.route('/timer/timerdata', methods=['GET'])
def get_time():
    if timerdata:
        return jsonify({'timerdata': timerdata})
    else:
        abort(404)

@app.route('/timer/timerdata', methods=['POST'])
def post_time():
    if not request.json or not "work_time" in request.json or not "start_time" in request.json:
        abort(400)
    timer_data_point = {
        "start_time": request.json["start_time"],
        "work_time": request.json["work_time"]
    }
    timerdata.append(timer_data_point)
    return jsonify({'timer_data_point': timer_data_point}), 201

@app.errorhandler(404)
def no_resource(error):
    return make_response(jsonify({'error': '404 Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)