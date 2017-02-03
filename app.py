"""
"""

import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '')


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('index.html')


@app.route('/api/twilio')
def send_text_file(file_name):
    """Send your static text file."""
    return 'hi'


if __name__ == '__main__':
    app.run(debug=True)
