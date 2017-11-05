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
    
//  Audio
    var frameCount = 0,     // Counts the frames from arecord
        lastFrame = 0,      // Last frame sent to browser
        audioData,          // all data from arecord is saved here and sent
			                // to the client when requested.
        audioChild = 0,     // Process for arecord
        audioRate = 8000;
        
        // PWM
        var pwm = 'P9_21';

// Initialize various IO things.
function initIO() {
    // Make sure gpios 7 and 20 are available.
    b.pinMode('P9_42', b.INPUT);
    b.pinMode('P9_41', b.INPUT);
    b.pinMode(pwm,     b.ANALOG_OUTPUT);    // PWM
}
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

//initIO();
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




    
    
    
    // now that we have our connected 'socket' object, we can 
    // define its event handlers

    // Send value every time a 'message' is received.
//     socket.on('ain', function (ainNum) {
//         b.analogRead(ainNum, function(x) {
//             if(x.err && errCount++<5) console.log("AIN read error");
//             if(typeof x.value !== 'number' || x.value === "NaN") {
//                 console.log('x.value = ' + x.value);
//             } else {
//                 socket.emit('ain', {pin:ainNum, value:x.value});
//             }
// //            if(ainNum === "P9_38") {
// //                console.log('emitted ain: ' + x.value + ', ' + ainNum);
// //            }
//         });
//     });

    socket.on('gpio', function (gpioNum) {
//    console.log('gpio' + gpioNum);
        // b.digitalRead(gpioNum, function(x) {
        //     if (x.err) throw x.err;
        //     socket.emit('gpio', {pin:gpioNum, value:x.value});
//            console.log('emitted gpio: ' + x.value + ', ' + gpioNum);
        // });
    });

    function trigger(arg) {
        var ledPath = "/sys/class/leds/beaglebone:green:usr";
//    console.log("trigger: " + arg);
	    arg = arg.split(" ");
	    for(var i=0; i<4; i++) {
//	    console.log(" trigger: ", arg[i]);
	        fs.writeFile(ledPath + i + "/trigger", arg[i]);
	    }
    }
    
    socket.on('trigger', function(trig) {
//	console.log('trigger: ' + trig);
	    if(trig) {
            trigger("heartbeat mmc0 cpu0 none");
        } else {
            trigger("none none none none");
        }
    });
    
    // Send a packet of data every time a 'audio' is received.

    socket.on('disconnect', function () {
        console.log("Connection " + socket.id + " terminated.");
        connectCount--;
        console.log("connectCount = " + connectCount);
    });

    connectCount++;
    console.log("connectCount = " + connectCount);
});
