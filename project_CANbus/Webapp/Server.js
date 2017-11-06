#!/usr/bin/node
// From Getting Started With node.js and socket.io
// http://codehenge.net/blog/2011/12/getting-started-with-node-js-and-socket-io-v0-7-part-2/
// This is a general server for the various web frontends
// buttonBox, ioPlot, realtimeDemo
"use strict";
// var can = require('socketcan');
// var myBuffer = require('buffer');
const repl = require('repl');
const path = require('path');
const WebSocket = require('ws');
const express = require('express');

// Setup express web server
const app = express();
const server = require('http').Server(app);
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, './public', 'CANbus.html'));
});
app.listen(9090, () => console.log('Example app listening on port 9090!'));
app.use(express.static('public'));

// CANbus setup
var channel;
var CANpayload = { 9999: {id: 9999, ms: Date.now(), data: [0,1,2,3,4,5,6,7] } };
function initCAN() {
    channel = can.createRawChannel("can0", true);

    // Log any message
    channel.addListener("onMessage", function(msg) {
        CANpayload[msg.id] = {
          id: msg.id,
          ms: (msg.ts_sec*1000 + parseInt(msg.ts_usec/1000)),
          data: Array.prototype.slice.call(msg.data,0),
        }
    } );

    // Reply any message
    channel.addListener("onMessage", channel.send, channel);

    channel.start();
}
// initCAN();

// Websocket
const wss = new WebSocket.Server({ port: 9091 });
wss.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    let msgObj = JSON.parse(message);
    if (typeof msgObj === 'object' && typeof msgObj.rq === 'string' && msgObj.rq === 'CAN') {
      sendCAN(ws, msgObj.payload);
    }
    // console.log('received: %s', JSON.stringify(msgObj));
  });
});

function sendCAN(ws, id) {
  // var arr = Array.prototype.slice.call(CANpayload[id], 0);
  // console.log("Got Request for CAN data: "+arr+ " for ID " +id);
  CANpayload[9999]['ms'] = Date.now();
  CANpayload[9999]['data'][1] = parseInt(Math.random()*256);
  ws.send(JSON.stringify({ rq: 'CAN', payload: CANpayload[id] }));
}

repl.start({
  prompt: 'CANbus> ',
  useGlobal: false,
}).context.CAN = CANpayload;
