from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iTrFSi8TcsrF5jSDG0i1D-p5SbidnTLvBgCFRdZTy7VmHebrEorv3M8huVJS2KQlPunGumIIcohLb'
socket_io = SocketIO(app)


@app.route('/monitoring')
def hello():
    return render_template('monitoring.html')


if __name__ == '__main__':
    app.run()
