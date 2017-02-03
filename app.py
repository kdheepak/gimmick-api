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
    # retrieve message.
    print(request.values)
    received_message = request.values.get('Body').strip()
    socketio.emit('sms', json.dumps({'data': received_message}))
    response = twiml.Response()
    response.sms("Message received")
    return str(response)



if __name__ == '__main__':
    socketio.run(app, debug=True)
