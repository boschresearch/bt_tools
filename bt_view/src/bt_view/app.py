from flask import Flask, render_template, Response
import time
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def generate():
    while True:
        # Simulate data update
        with open(os.getcwd() + '/live_visualization.svg', 'r', encoding='utf-8') as f:
            svg_content = f.read().replace('\n', '')
        data = f"data: {svg_content}\n\n"
        yield data
        time.sleep(1)


@app.route('/events')
def events():
    return Response(generate(), content_type='text/event-stream')
