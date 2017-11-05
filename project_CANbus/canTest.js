var can = require('socketcan');
var myBuffer = require('buffer');


var channel = can.createRawChannel("can0", true);

// Log any message
channel.addListener("onMessage", function(msg) {
    
    var payload = msg.data
    var arr = Array.prototype.slice.call(payload, 0)
    console.log(payload)

} );

// Reply any message
channel.addListener("onMessage", channel.send, channel);

channel.start();