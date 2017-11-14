# Project CANbus:

The goal of this project is to 1) configure the canbus and socketcan on the beaglebone blue and 2) develop an internally hosted webapp that allows the user to monitor parameters that are being published on the canbus. 

To install project, run 
`bone$ cd project_CANbus/Webapp/`
`bone$ sudo npm install`

To run project:

`bone$ sudo ./enableCAN`
`bone$ node /project_CANbus/Server.js`

Then point your browser to http://IPADDRESS:9090 and the webpage should be served.

Within the /Webapp/ Directory, there are a few subdirectories, with the most important being public. This is the folder that contains all files that the client may request, including the main HTML and JS file.  All additional files are stored within the css or js subdirectories. 

The main server file is "Server.js"
