#!/usr/bin/env python3
#Adam Wiesler
#Etch-A-Sketch controlled with 4 pushbuttons

#various parameters for setup:
#Low temperature setpoint
tempLow = 74
#High temperature setpoint
tempHigh = 80

#display verticle axis range:
displayMin = 65
displayMax = 85

displayChart1 = [0,0,0,0,0,0,0,0]
displayChart2 = [0,0,0,0,0,0,0,0]


import Adafruit_BBIO.GPIO as GPIO
import smbus
import time
import math
bus = smbus.SMBus(1) 
matrix = 0x70
tmp101_0 = 0x49    
tmp101_1 = 0x4a
tmp101_0_ALERT = "GP1_3"
tmp101_1_ALERT = "GP1_4"

# Setup LED Matrix
bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)


def tempAlert(buttonKey):
    if(buttonKey == tmp101_0_ALERT):
        if(GPIO.input(buttonKey) == 1):
            print("Temp Sensor ", ("0x{:02x}".format(tmp101_0)), " fell below lower threshold ", tempLow, "(",getTemperature(tmp101_0),")")
        elif GPIO.input(buttonKey) == 0:
            print("Temp Sensor ", "0x{:02x}".format(tmp101_0), " went above upper threshold ", tempHigh, "(",getTemperature(tmp101_0),")")
    if(buttonKey == tmp101_1_ALERT):
        if GPIO.input(buttonKey) == 1:
            print("Temp Sensor ", "0x{:02x}".format(tmp101_1), " fell below lower threshold ", tempLow, "(",getTemperature(tmp101_1),")")
        elif GPIO.input(buttonKey) == 0:
            print("Temp Sensor ", "0x{:02x}".format(tmp101_1), " went above upper threshold ", tempHigh, "(",getTemperature(tmp101_1),")")
    return

#Setup inputs:
GPIO.setup(tmp101_0_ALERT, GPIO.IN)
GPIO.add_event_detect(tmp101_0_ALERT, GPIO.BOTH, callback=tempAlert)
GPIO.setup(tmp101_1_ALERT, GPIO.IN)
GPIO.add_event_detect(tmp101_1_ALERT, GPIO.BOTH, callback=tempAlert)


#Display control functions:
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
    
#temperature conversion functions
def cToF(tempC):
    return 32+tempC*1.8
def fToC(tempF):
    return (tempF-32)/1.8

# There are "cleaner" ways to do this, but coding it this way makes it easier to follow how the unit conversion works
def cTo12Bit(tempC):
    newC = abs(tempC)
    _12Bit = 0b000000000000

    if tempC < 0:
        _12Bit = _12Bit | 0b100000000000
    
    for index in range (0,11):
        #print("NewC = ", newC, "")
        if (newC-math.pow(2,((10-index)-4))) > 0:
            newC = newC-(math.pow(2,((10-index)-4)))
            _12Bit = _12Bit | (1<<(10-index))
            #print("Adding ",(math.pow(2,((10-index)-4))))
        #print(newC)

    upperByte = (_12Bit) >> 4
    lowerByte = (_12Bit & (0b000000001111)) << 4
    return [upperByte,lowerByte]

def _12BitToC(_12BitIn):
    _12Bit = (_12BitIn[0]<<4) | (_12BitIn[1] >> 4)
    _11Bit = _12Bit & 0b011111111111
    degC = int(_11Bit)*.0625
    if (_12Bit>>11) > 0:
        degC = degC*(-1)
    return degC
#TMP101 Functions
def flipBytes(wordIn):
    upper = wordIn & 0b11111111
    lower = wordIn >> 8
    return [upper,lower]
    
def setTMP101Settings(device,tHigh,tLow):
    mode = 0b0110000  #Put the device into 12 bit mode
    #bus.write_byte_data(device,0,0b00000001) #Set register to Configuration
    bus.write_byte_data(device,1,mode) #Set register to Configuration
    
    tLow12Bit = cTo12Bit(fToC(tLow))
    tHigh12Bit = cTo12Bit(fToC(tHigh))
    print("tHigh: ", bin(tHigh12Bit[0]), bin(tHigh12Bit[1]))
    bus.write_i2c_block_data(device,2,[tLow12Bit[0],tLow12Bit[1]])      # Set temp lower
    bus.write_i2c_block_data(device,3,[tHigh12Bit[0],tHigh12Bit[1]])    # Set temp upper


    print("Configuration for device ", "0x{:02x}".format(device), " :","{0:b}".format(bus.read_byte_data(device,1)))
    print("Low Temperature Threshold for device ", "0x{:02x}".format(device), " :",cToF(_12BitToC(flipBytes(bus.read_word_data(device,2)))))
    print("Low Temperature Threshold for device ", "0x{:02x}".format(device), " :",bin(bus.read_word_data(device,2)))
    print("High Temperature Threshold for device ", "0x{:02x}".format(device), " :",cToF(_12BitToC(flipBytes(bus.read_word_data(device,3)))))
    


def getTemperature(device):
    return cToF(_12BitToC(flipBytes(bus.read_word_data(device,0))))
   
   
setTMP101Settings(tmp101_0,tempHigh,tempLow)
setTMP101Settings(tmp101_1,tempHigh,tempLow)

def drawBarGraph(y1,y2,minInput,maxInput):
    global displayChart1
    global displayChart2
    
    if y1 < minInput:
        y1 = minInput
    elif y1 > maxInput:
        y1 = maxInput
    if y2 < minInput:
        y2 = minInput
    elif y2 > maxInput:
        y2 = maxInput
        
    scaleFactor = (maxInput-minInput)/7.0
    
    y1Scaled = int((y1-minInput)/scaleFactor)
    y2Scaled = int((y2-minInput)/scaleFactor)
    
    del displayChart1[0]
    del displayChart2[0]
    
    displayChart1.extend([y1Scaled])
    displayChart2.extend([y2Scaled])
    #print(displayChart1, " and ",displayChart2)

    global matrixOutput
    matrixOutput = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    for x in range (0,8):
        if displayChart1[x] == displayChart2[x]:
            writeLEDPixel(7-x,7-displayChart1[x],1,1)
        else:
            writeLEDPixel(7-x,7-displayChart1[x],1,0)
            writeLEDPixel(7-x,7-displayChart2[x],0,1)
            
    

try:
    while True:
        time.sleep(.3)   # Let other processes run
        drawBarGraph(getTemperature(tmp101_0),getTemperature(tmp101_1),displayMin,displayMax)
        #print("Temp of 0x49: ", getTemperature(tmp101_0))
        #print("Temp of 0x4a: ", getTemperature(tmp101_1))

except KeyboardInterrupt:
    #GPIO.cleanup()
    exit()

