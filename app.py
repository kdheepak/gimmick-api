#!/usr/bin/env python
import os
import json
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from twilio import twiml

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fls9024rdsv123dsk')
socketio = SocketIO(app, async_mode=async_mode)
thread = None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    docstring_mouse = '''Send "up", "down", "left" or "right" to move the mouse.
When the mouse gets the cheese, the person with the winning move gets 2 points.
When the mouse is poisoned, the person with the winning move gets one point and the previous winner loses one point.
'''

    docstring_survey = '''Reply with a comma separated list of libraries or languages.

e.g.

    libraries: ggplot2, matplotlib, d3.js

OR

    languages: R, Python
'''

    docstring = '''Type "docs survey" or "docs mouse" for more information'''

    message_body = request.values.get('Body').strip()
    message_from = request.values.get('From').strip()

    body = message_body.replace(' ', '').lower()

    if 'docs' in body and 'survey' in body:
        resp = twiml.Response()
        resp.message(docstring_survey)
        return '' # str(resp)
    elif 'docs' in body and 'mouse' in body:
        resp = twiml.Response()
        resp.message(docstring_mouse)
        return '' # str(resp)
    elif 'docs' == body:
        resp = twiml.Response()
        resp.message(docstring)
        return '' # str(resp)

    if ('libraries:' not in body and 'languages:' not in body) or (':' in body.split(':')[1] or body.split(':')[1] == ''):
        if body in ['up', 'down', 'left', 'right']:
            socketio.emit('sms', json.dumps({'from': message_from, 'body': body}))
            return ''
        else:
            resp = twiml.Response()
            resp.message("I did not understand that. Type 'docs' for more information.")
            return '' # str(resp)
    else:
        socketio.emit('sms', json.dumps({'from': message_from, 'body': message_body}))
    return ''


if __name__ == '__main__':
    socketio.run(app)
