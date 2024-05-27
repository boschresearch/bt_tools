from flask import Flask, render_template, Response
import redis_server
from flask_sse import sse
import os



# class App():
#     def __init__(self) -> None:
#         self.app = Flask(__name__)
#         self.app.debug = True

app = Flask(__name__)
app.register_blueprint(sse, url_prefix='/stream')
app.config["REDIS_URL"] = "redis://localhost:6379/"


@app.route('/')
def index():
    abc = 'abc'
    return render_template('index.html').replace('<div id="content"></div>', f'<div id="content">{abc}</div>')


def send_sse_message(data):
    with app.app_context():
        sse.publish(data, type='update')

# def generate():
#     # Simulate data update
#     with open(os.getcwd() + '/live_visualization.svg', 'r', encoding='utf-8') as f:
#         svg_content = f.read().replace('\n', '')
#     data = f"data: {svg_content}\n\n"
#     yield data


# @app.route('/events')
# def events():
#     return Response(generate(), content_type='text/event-stream')
