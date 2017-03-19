#!/usr/bin/env python
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
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    docstring = '''Reply with a comma separated list of libraries or languages.

e.g.

    libraries: ggplot2, matplotlib, d3.js

OR

    languages: R, Python
'''
    message_body = request.values.get('Body').strip()
    message_from = request.values.get('From').strip()
    if 'documentation' in message_body.replace(' ', '').lower().split():
        resp = twiml.Response()
        resp.message(docstring)
        return str(resp)

    body = message_body.replace(' ', '').lower()

    if ('libraries:' not in body and 'languages:' not in body) or (':' in body.split(':')[1] or body.split(':')[1] == ''):
        resp = twiml.Response()
        resp.message("I did not understand that. Can you try again?\n\n" + docstring)
        return str(resp)
    else:
        socketio.emit('sms', json.dumps({'from': message_from, 'body': message_body}))
    return ''


if __name__ == '__main__':
    socketio.run(app)
