"""
"""

import os
from flask import Flask, render_template, request, redirect, url_for

from twilio import twiml

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('index.html')


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    # retrieve message.
    received_message = request.values.get('Body').strip().lower()
    print(received_message)
    response = twiml.Response()
    response.sms("Congratulations! ")
    return str(response)


if __name__ == '__main__':
    app.run(debug=True)
