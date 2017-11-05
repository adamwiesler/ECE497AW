    var socket;
    
    var CANData = [];
    var indexCANData = 0;
    
    var firstconnect = true,
        samples = 100,          // Number of values to plot
        io;

    var dataPeriod = 100;
    var dataTimer;

    function connect() {
      if(firstconnect) {
        socket = io.connect(null);

        socket.on('message', function(data)
            { status_update("Received: message " + data);});
        socket.on('connect', function()
            { status_update("Connected to Server"); });
        socket.on('disconnect', function()
            { status_update("Disconnected from Server"); });
        socket.on('reconnect', function()
            { status_update("Reconnected to Server"); });
        socket.on('reconnecting', function( nextRetry )
            { status_update("Reconnecting in " + nextRetry/1000 + " s"); });
        socket.on('reconnect_failed', function()
            { status_update("Reconnect Failed"); });

        socket.on('CAN',  CAN);

        firstconnect = false;
        
        dataTimer = setInterval(requestCANData, dataPeriod);
      }
      else {
        socket.socket.reconnect();
        dataTimer = setInterval(requestCANData, dataPeriod);
        }
    }

    function disconnect() {
      clearInterval(dataTimer);
      //clearInterval(topTimer);
      socket.disconnect();
    }

    // When new data arrives, convert it and plot it.
    function CAN(data) {
        CANData = data;
        indexCANData++;
        if(indexCANData >= samples){
            indexCANData = 0;
        }

        //plotTop.setData(CANData[0]);
        //plotTop.draw();
        status_update("Can data[0]: " + CANData[0])
    }


    function status_update(txt){
      document.getElementById('status').innerHTML = txt;
    }

    // Request data every dataPeriod ms
    function requestCANData() {
        var i;
        socket.emit("CAN", 1349); //Request can message ID 1349 from the server
    }
