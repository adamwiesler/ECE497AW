#!/usr/bin/env python3
#Adam Wiesler
#Etch-A-Sketch controlled with 4 pushbuttons

#get size based on terminal call. Default to 8. Inputs aren't well sanitized
import sys
gridSizeRow = 8;
gridSizeCol = 8;
    
position = [0,0]

print("Rows: ", gridSizeRow, "Cols: ", gridSizeCol)



import time
import curses
# Import PyBBIO library:
import Adafruit_BBIO.GPIO as GPIO

import smbus
import time
bus = smbus.SMBus(1)  # Use i2c bus 1
matrix = 0x70         # Use address 0x70

import rcpy 
import rcpy.encoder as encoder
rcpy.set_state(rcpy.RUNNING)


#Setup LED Matrix
bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)
matrixOutput = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
bus.write_i2c_block_data(matrix, 0, matrixOutput)

def clearLEDDisplay():
    global matrixOutput
    matrixOutput = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    bus.write_i2c_block_data(matrix, 0, matrixOutput)
def writeLEDPixel(row,col,green,red):
    greenRow = 1<<col
    redRow = 1<<col
    if green > 0:
        matrixOutput[0+row*2] = int(matrixOutput[0+row*2]) | greenRow 
    elif matrixOutput[0+row*2] & greenRow > 0:
        matrixOutput[0+row*2] = int(matrixOutput[0+row*2]) ^ greenRow 
    if red > 0:
        matrixOutput[1+row*2] = matrixOutput[1+row*2] | redRow 
    elif matrixOutput[1+row*2] & redRow > 0:
        matrixOutput[1+row*2] = int(matrixOutput[1+row*2]) ^ redRow 
    bus.write_i2c_block_data(matrix, 0, matrixOutput)
    
    


#Setup the display using curses
stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

curses.noecho()
curses.cbreak()
stdscr.keypad(1)

#Create first window at top left for instructions:
win1 = curses.newwin(3, 70, 0, 0)
win1.addstr(0, 0, "Use buttons connected to GP0 to move around                    ",curses.color_pair(1))
win1.addstr(1, 0, "Pressing GP0_4 and GP0_6 at the same time clears the display.  ",curses.color_pair(1))
win1.addstr(2, 0, "Pressing GP0_3 and GP0_5 at the same time exits the program.   ",curses.color_pair(1))
win1.refresh()

def clear():
    global win2
    global position
    for y in range(0, gridSizeRow+2):
        for x in range(0, gridSizeCol+2):
            try:
                if (x==0 or x == gridSizeCol+1) or (y==0 or y == gridSizeRow+1):
                    win2.addstr(y,x, '*',curses.color_pair(2))
                else:
                    win2.addstr(y,x, ' ',curses.color_pair(2))
            except curses.error:
                pass   
    win2.refresh()
    position = [0,0]
    win2.addstr(position[0]+1,position[1]+1,'X',curses.color_pair(3))
    win2.move(position[0]+1,position[1]+1)
    win2.refresh()
    clearLEDDisplay()
    writeLEDPixel(7-position[1],position[0],1,0)


#Create second Window and clear
win2 = curses.newwin(gridSizeRow+2,gridSizeCol+2, 4, 0)
clear()



#Setup buttons and move directions:
buttons = ["GP0_3","GP0_4","GP0_5","GP0_6"]
directions = [[1,0],[-1,0],[0,1],[0,-1]]
GPIOEdges = [GPIO.FALLING, GPIO.RISING,GPIO.FALLING, GPIO.RISING]
buttonPressedVal = [0, 1, 0, 1]
directionMap = dict(zip(buttons,directions))
edgeMap = dict(zip(buttons,GPIOEdges))
pressedMap = dict(zip(buttons,buttonPressedVal))


#setup interrupt handler
def setPosition(buttonKey):
    if (GPIO.input(buttons[1]) == 1) and (GPIO.input(buttons[3]) == 1):
        clear()
        return
    elif (GPIO.input(buttons[0]) == 0) and (GPIO.input(buttons[2]) == 0):
        leave()
        return
    else:
        if GPIO.input(buttonKey) == pressedMap[buttonKey]:
            move(directionMap[buttonKey][0],directionMap[buttonKey][1])
            return
    
#set button pin direction, attach interrupts:
for x in buttons[:]:
    GPIO.setup(x, GPIO.IN)
    GPIO.add_event_detect(x, edgeMap[x], callback=setPosition)

def move(row, col):
    writeLEDPixel(7-position[1],position[0],0,1)
    global position
    global win2
    workingPositon = [position[0]+row,position[1]+col]
    workingPositon[0] = min(gridSizeRow-1,max(0,workingPositon[0]))
    workingPositon[1] = min(gridSizeCol-1,max(0,workingPositon[1]))
    position = workingPositon;
    
    
    #if (position[0] == workingPositon[0]) and (position[1] == workingPositon[1]):
    #    return

    #print("Position = ", position)
    win2.addstr(position[0]+1,position[1]+1,'X',curses.color_pair(3))
    win2.move(position[0]+1,position[1]+1)
    win2.refresh()
    writeLEDPixel(7-position[1],position[0],1,0)


    return


def leave():
    #print("leaving")
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
    exit()
    

encoderOld2 = 0
encoderOld3 = 0

try:
    while True:
        
        time.sleep(.15)   # Let other processes run
        if rcpy.get_state() == rcpy.RUNNING:
            e2 = encoder.get(2) # read the encoders
            e3 = encoder.get(3)
            if(e2-encoderOld2>=2):
                #print("Encoder 2: ", e2," ", encoderOld2," ", (e2-encoderOld2))
                encoderOld2 = e2
                move(0,1)
            elif((e2-encoderOld2 <=-2)):
                #print("Encoder 2: ", e2," ", encoderOld2," ", (e2-encoderOld2))
                encoderOld2 = e2
                move(0,-1)
            if(e3-encoderOld3>=2):
                encoderOld3 = e3
                move(1,0)
            elif(e3-encoderOld3<=-2):
                encoderOld3 = e3
                move(-1,0)
            
except KeyboardInterrupt:
    #print("Cleaning Up")
    GPIO.cleanup()
    leave()
GPIO.cleanup()
exit()
