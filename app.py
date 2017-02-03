"""
"""

import os
import json
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from twilio import twiml

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def connect():
    emit('status', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app)

