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


@socketio.on('connect')
def on_connect():
    send('connected')


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('index.html')


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    # retrieve message.
    received_message = request.values.get('Body').strip()
    socketio.emit('sms', json.dumps({'data': received_message}))
    response = twiml.Response()
    response.sms("Message received")
    return str(response)


if __name__ == '__main__':
    app.run(debug=True)
