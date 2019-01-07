from flask import Flask
from flask_prometheus import monitor

from monitoring.config import CONFIG

app = Flask(__name__)
app.config.update(CONFIG)

if __name__ == '__main__':
    monitor(app, port=8000)
    app.run()
