#!/usr/bin/node
// From Getting Started With node.js and socket.io 
// http://codehenge.net/blog/2011/12/getting-started-with-node-js-and-socket-io-v0-7-part-2/
// This is a general server for the various web frontends
// buttonBox, ioPlot, realtimeDemo
"use strict";
var can = require('socketcan');
var myBuffer = require('buffer');


var port = 9090, // Port to listen on
    bus = '/dev/i2c-1',
    busNum = 1,     // i2c bus number
    i2cNum = 0,             // Remembers the address of the last request
    http = require('http'),
    url = require('url'),
    fs = require('fs'),
    b = require('bonescript'),
    child_process = require('child_process'),
    server,
    connectCount = 0,	// Number of connections to server
    errCount = 0;	// Counts the AIN errors.
    
var channel;
var CANpayload = [];
function initCAN() {
    channel = can.createRawChannel("can0", true);
    
    // Log any message
    channel.addListener("onMessage", function(msg) {
        CANpayload[msg.id] = msg.data;
       //console.log(CANpayload[msg.id])

    } );
    
    // Reply any message
    channel.addListener("onMessage", channel.send, channel);
    
    channel.start();
}

function send404(res) {
    res.writeHead(404);
    res.write('404');
    res.end();
}

initCAN();


server = http.createServer(function (req, res) {
// server code
    var path = url.parse(req.url).pathname;
    console.log("path: " + path);
    if (path === '/') {
        path = '/CANbus.html';
    }

    fs.readFile(__dirname + path, function (err, data) {
        if (err) {return send404(res); }
//            console.log("path2: " + path);
        res.write(data, 'utf8');
        res.end();
    });
});

server.listen(port);
console.log("Listening on " + port);

// socket.io, I choose you
var io = require('socket.io').listen(server);
io.set('log level', 2);

// See https://github.com/LearnBoost/socket.io/wiki/Exposed-events
// for Exposed events

// on a 'connection' event
io.sockets.on('connection', function (socket) {

    console.log("Connection " + socket.id + " accepted.");
//    console.log("socket: " + socket);

//Respond to CANbus message request:
    socket.on('CAN', function (messageID) {
            var arr = Array.prototype.slice.call(CANpayload[messageID], 0)
            console.log("Got Request for CAN data: "+arr+ " for ID " +messageID)
            socket.emit('CAN', arr);
    });
    socket.on('disconnect', function () {
        console.log("Connection " + socket.id + " terminated.");
        connectCount--;
        console.log("connectCount = " + connectCount);
    });

    connectCount++;
    console.log("connectCount = " + connectCount);
});
