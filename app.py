from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post('/register')
def hello_world():
    data = request.get_json()
    return jsonify(data)