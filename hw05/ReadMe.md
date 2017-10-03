# Homework hw05:    

### LED Matrix Control

Answers to questions:

1. On the first connect, the socket.io communication link is established. After that, the bone reads the current status of the LED matrix by socket.io calling the "matric()" function.  The data gets popluated and put into a memory variable local to the client.  When the browser wants to make a change to the matrix, it uses "i2cset" socket and directly sends the i2c frames that it needs. The script on the bone just sends that data out over the physical i2c port. Technically the browser could control any i2c device without server modification.
2. When an LED is clicked in the browser, the function LEDclick(i, j) gets called.  This function then determines what new data needs to be sent to the LED matrix, and sends it using a socket.emit call.
3. The below `background-color: green;` is what sets the LED color in the browser
```
.on {
	border: 1px solid #00ee00;
	background-color: green;

}
```
4. I plan to modify the exesting code in such a way that the entire status of the LED matrix is read into a 2d integer array at the beginning, where each entry can be 0-3, with a 0 is off, 1 being green, two red, and three yellow.  Then, when an LED is clicked, the LEDclick function will read the 2d array, make an 8 bit integer with the new column value, and send it over i2c using the socket.emit call. The browser will also be changed by adding additional css entries to the css file for the different colors.
5. See commit for code. No changes to boneServer were necessary.


To run server: `$bone sudo node boneServer.js`
Then point browser to http://boneip:9090/matrixLED.html

