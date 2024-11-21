import datetime
from flask import Flask
import io
import numpy as np
import cv2
from PIL import Image
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
import cv2
import numpy as np


######################
# interact with front#
######################
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
app = Flask(__name__)
app.after_request(after_request)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins=['http://localhost:3000']) 
meetings = []
users = {}
my_id = 0
@socketio.on('connect')
def handle_connect():
    '''
    connect and get meetings from the server
    '''
    # TODO: get meetings from the server
    emit('newMeeting',meetings,broadcast=True)
    print('new client connect')

@socketio.on('createMeeting')
def handle_new_meeting(data):
    meeting_id = len(meetings) + 1  
    participants = []  
    chat = []
    default_message = {
        'id': 1,
        'type': 'commented',
        'person': {
            'name': 'System',
            'imageUrl': 'https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'  
        },
        'comment': 'Welcome to the meeting! The meeting has been successfully created.',
        'date': 'secret date',  
        'dateTime': 'secretDateTime'  
    }
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
    print('new meeting added')
    emit('newMeeting', meetings, broadcast=True)
    
@socketio.on('join')
def handle_join(data):
    meeting_id = int(data.get('meetingId'))
    print(f"User joined meeting: {meeting_id}")
    for m in meetings:
        if int(m['id']) == meeting_id:
            print('enter')
            meeting = m
            print(meeting['chat'])
            # emit('update_chat_message', {'Id': meeting_id, 'message': meeting['chat']},broadcast=True)
            emit('update_chat_message', {'Id': meeting_id, 'message': meeting['chat']},broadcast=True)

            
@socketio.on('createMessage')
def handle_create_message(data):
    meeting_id = int(data.get('meetingId'))
    new_message = data.get('message')
    message = {
        'id': new_message['id'], 
        'type': new_message['type'],
        'person': new_message['person'],
        'comment': new_message['comment'],
        'date': new_message['date'], 
        'dateTime': new_message['dateTime']  
    }
    print('get client message!')
    print(message)
    for meeting in meetings:
        if meeting['id'] == meeting_id:
            meeting['chat'].append(message)
            break
    emit('update_chat_message', {'Id': meeting_id, 'message': meeting['chat']},broadcast=True)

@socketio.on('register_user')
def handle_register_user(user_data):
    users[1] = user_data  
    emit('user_list', users, broadcast=True) 
    

@socketio.on('video_frame')
def handle_video_frame(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        image_cv = np.array(image)
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)
        processed_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        _, buffer = cv2.imencode('.jpg', processed_image)
        frame_data = buffer.tobytes()
        socketio.emit('processed_frame', frame_data)
    except Exception as e:
        print(f"Error processing frame: {e}")
# TODO: user leaving the meeting
# @socketio.on('leave_meeting')
# def handle_leave_meeting(data):
#     meeting_id = int(data.get('meetingId'))
#     for meeting in meetings:
#         if meeting['id'] == meeting_id:
#             meeting['participants'].remove(data.get('username'))
#             break
#     emit('update_participants', {'Id': meeting_id, 'participants': meeting['participants']},broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if 1 in users:
        del users[1]  
    
if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5001)
