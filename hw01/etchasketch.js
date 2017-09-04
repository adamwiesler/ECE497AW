var gridSizeRow = process.argv[2];
var gridSizeCol = process.argv[3];

var gridSizeRow = 5;
var gridSizeCol = 5;

var position = [0,0];

const readline = require('readline');

//Listen to STDIN
readline.emitKeypressEvents(process.stdin);

process.stdin.setRawMode(true);

console.log("Starting...");
var clc = require('cli-color');
clear();
// Start the keypress listener for the process
process.stdin.on('keypress', (str, key) => {

    // "Raw" mode so we must do our own kill switch
    if(key.sequence === '\u0003') {
        process.exit();
    }

    // User has triggered a keypress, now do whatever we want!
    // ...
    //console.log(key.name);
    
    switch (key.name){
        case "up":
            move(1,0);
            break;
        case "down":
            move(-1,0);
            break;
        case "left":
            move(0,-1);
            break;
        case "right":
            move(0,1);
            break;
        case "c":
            clear();
            break;
        default: break;        
    }

});

function move(row, col){
    var workingPositon = [position[0]+row,position[1]+col];
    workingPositon[0] = Math.min(gridSizeRow,Math.max(0,workingPositon[0]));
    workingPositon[1] = Math.min(gridSizeCol,Math.max(0,workingPositon[1]));
    if(position[0] == workingPositon[0] && position[1] == workingPositon[1]){
        return;
    }
    position = workingPositon;
    
    //console.log(`row = ${position[0]} col = ${position[1]}`);
    
}

function clear(){
    //Clear entire terminal:
    process.stdout.write(clc.reset);
    
    //Wrire frame:
    process.stdout.write(clc.reset);
    console.log(clc.green('Use arrow keys to move, press "c" to clear display, "Ctrl+c" to exit'));   
    for (var i = 0;i<4;i++){
        clc.move.to(0, i);
        console.log(clc.blue('*'));
        clc.move.to(4, i);
        console.log(clc.blue('*'));

    }
}