from flask import Flask, render_template
from flask_sse import sse


app = Flask(__name__)
app.register_blueprint(sse, url_prefix='/stream')
app.config["REDIS_URL"] = "redis://localhost:6379/"


@app.route('/')
def index():
    abc = 'abc'
    return render_template('index.html').replace(
        '<div id="content"></div>', f'<div id="content">{abc}</div>')


def send_sse_message(data):
    with app.app_context():
        sse.publish(data, type='update')
