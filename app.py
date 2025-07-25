from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/status')
def status():
    return jsonify({'status': 'OK', 'service': 'Flask Demo App'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
