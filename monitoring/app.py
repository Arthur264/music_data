import time

from flask import Flask, render_template
from flask_socketio import SocketIO

from database.connect import db
from monitoring.config import CONFIG
from storage.queue import redis_queue

app = Flask(__name__)
app.config.update(CONFIG)
socket_io = SocketIO(app)


@app.route('/monitoring')
def monitoring():
    return render_template('monitoring.html')


def background_thread():
    while True:
        if not redis_queue.empty():
            task = redis_queue.get()
            socket_io.emit(task['name'], task['data'])
        else:
            time.sleep(1)


def emit_all_collection():
    cursor = db.cursor()
    for collection in cursor.collection_names():
        socket_io.emit(collection, list(cursor[collection].find({}, {'_id': False})))


@socket_io.on('connect')
def test_connect():
    emit_all_collection()
    socket_io.start_background_task(target=background_thread)


if __name__ == '__main__':
    socket_io.run(app, port=8081)
