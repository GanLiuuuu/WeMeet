import datetime
from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
import cv2
import numpy as np
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
app = Flask(__name__)
app.after_request(after_request)

cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

socketio = SocketIO(app, cors_allowed_origins=['http://localhost:3000']) 
meetings = []

@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    send(f"Echo: {msg}")

@socketio.on('createMeeting')
def handle_new_meeting(data):
    meeting_id = len(meetings) + 1  
    participants = []  # 初始化参会人员列表
    chat = []
        # 添加一个默认的系统消息到聊天记录
    default_message = {
        'id': 1,
        'type': 'commented',
        'person': {
            'name': 'System',
            'imageUrl': 'https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'  # 系统头像可以使用默认的图片
        },
        'comment': 'Welcome to the meeting! The meeting has been successfully created.',
        'date': 'secret date',  # 当前时间作为消息日期
        'dateTime': 'secretDateTime'  # ISO格式的时间
    }
    
    # 将默认消息添加到聊天记录
    chat.append(default_message)
    new_meeting = {
        'id': meeting_id,
        'href': '/meeting/' + str(meeting_id),
        'meetingName': data.get('meetingName'),
        'hostName': data.get('hostName'),
        'status': data.get('status'),
        'description': data.get('description'),
        'meeting_data': data  ,
        'participants': participants,
        'chat': chat    
    }
    meetings.append(new_meeting)  
    print(meetings)
    print('new meeting added')
    emit('newMeeting', meetings, broadcast=True)

@socketio.on('connect')
def handle_connect():
    emit('newMeeting',meetings,broadcast=True)
    print('new client connect')
   
# 监听 'video' 事件
@socketio.on('video')
def handle_video_frame(frame):
    # 接收视频帧并处理，假设前端发送的是图像的二进制数据
    np_frame = np.frombuffer(frame, dtype=np.uint8)
    img = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)
    
    if img is not None:
        # 处理视频帧 (例如，显示、保存、推送给其他客户端等)
        cv2.imshow("Video Stream", img)
        cv2.waitKey(1)  # OpenCV显示图像的方式
    
    emit('response', {'data': 'Frame received'})  # 可以返回一个响应给客户端
    
@socketio.on('join')
def handle_join(data):
    meeting_id = int(data.get('meetingId'))
    print(f"User joined meeting: {meeting_id}")
    for m in meetings:
        if int(m['id']) == meeting_id:
            print('enter')
            meeting = m
            print(meeting['chat'])
            emit('update_chat_message', meeting['chat'],broadcast=False)
if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5001)
