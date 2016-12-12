* Code for the original Color Commons in 2013: https://gist.github.com/4494118
* tech blog post http://rascalmicro.com/docs/project-light-blades.html

### Setup of microcontroller ###

* Download Raspbian image with OLA added from http://dl.openlighting.org/ Used raspbian-ola-0.9.5.zip
* Power up RPi with USB cable and wall wart.
* Connect to RPi using Putty on COM4 at 115200 bps or `screen /dev/tty.usbserialaskjfhaskjh 115200` Physical connection is with a USB cable to a FTDI breakout board to wires to pins 6, 8, 10 on RPi header.
* Username is pi; default password is openlighting

Install `autossh`

    sudo apt-get install autossh


