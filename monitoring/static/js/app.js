var app = {
    socket: function () {
        var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', function () {
            socket.emit('file_size', {data: 'I\'m connected!'});
        });

        socket.on('file_size', function (data) {
            console.log(data)
        });

        socket.on('memory', function (data) {
            console.log(data)
        });


    },
    init: function () {
        this.socket();
    }

}

$(document).ready(function () {
    app.init()

})