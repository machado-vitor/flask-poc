from flask import Flask, jsonify, render_template, request, Response
import platform
import socket
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, REGISTRY

app = Flask(__name__, template_folder='templates')

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    'flask_http_request_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'flask_http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

# Middleware to record request metrics
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.path
    ).observe(request_latency)
    return response

# Endpoint to expose Prometheus metrics
@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype=CONTENT_TYPE_LATEST)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/hello')
def hello_world():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/status')
def status():
    return jsonify({'status': 'OK', 'service': 'Flask Demo App'})

@app.route('/api/info')
def info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return jsonify({
        'hostname': hostname,
        'ip': ip_address,
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'environment': os.environ.get('ENVIRONMENT', 'development')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
