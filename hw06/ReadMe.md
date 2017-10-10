# Homework hw06:    

### LCD etchasketch:

Install pygame for python3:
the rcpy only works on python3. There are no pre-built pygame installations for python3.  The below worked for me to get pygames working: 

```
sudo apt-get install mercurial python3-dev python3-numpy libav-tools \
    libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
    libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
hg clone https://bitbucket.org/pygame/pygame
cd pygame
python3 setup.py build
sudo python3 setup.py install
```
From <https://askubuntu.com/questions/97717/how-can-i-get-pygame-for-python3>


To run my etchasketch, first turn the display "on" using the on script from the displays folder, then run `sudo python3 etchasketch_LCDdisp_Encoders.py RR CC` where RR and CC represent the number of rows and columns desired. default (no entry) is 24x32, giving 10x10 sized cells.
Ctrl+c exits program.