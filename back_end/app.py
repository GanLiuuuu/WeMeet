from flask import Flask
from flask_socketio import SocketIO, send
from flask_cors import CORS
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
app = Flask(__name__)
app.after_request(after_request)

cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

socketio = SocketIO(app, cors_allowed_origins=['http://localhost:3000']) 

# 处理消息
@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    send(f"Echo: {msg}")
@socketio.on('connect')
def test_connect():
    print ("client connected:")
    
if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5001)
