from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
app = Flask(__name__)
app.after_request(after_request)

cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

socketio = SocketIO(app, cors_allowed_origins=['http://localhost:3000']) 
meetings = []

# 处理消息
@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    send(f"Echo: {msg}")

@socketio.on('createMeeting')
def handle_new_meeting(data):
    meetings.append(data)  # 将新会议添加到列表
    print('new meeting added')
    # 广播新会议数据给所有连接的客户端
    emit('newMeeting', data, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print('new client connect')
    emit('newMeeting', meetings, broadcast=False)
if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5001)
