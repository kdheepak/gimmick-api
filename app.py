"""
"""

import os
from flask import Flask, render_template, request, redirect, url_for

import twilio

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('index.html')


@app.route('/api/twilio')
def api():
    """Send your static text file."""
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
