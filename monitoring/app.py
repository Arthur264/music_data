import time

from flask import Flask, render_template
from flask_socketio import SocketIO

from monitoring.config import CONFIG
from pubsub.pubsub import pub_sub

app = Flask(__name__)
app.config.update(CONFIG)
socket_io = SocketIO(app)


@app.route('/monitoring')
def hello():
    return render_template('monitoring.html')


def background_thread():
    while True:
        task = pub_sub.get()
        if task:
            socket_io.emit(task['name'], task['data'])
        else:
            time.sleep(1)


@socket_io.on('connect')
def test_connect():
    socket_io.start_background_task(target=background_thread)


if __name__ == '__main__':
    socket_io.run(app, port=8081)
