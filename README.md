* Code for the original Color Commons in 2013: https://gist.github.com/4494118
* tech blog post http://rascalmicro.com/docs/project-light-blades.html
* Lights in lightblades are Lumenpulse Lumenfacade Stand Alone RGB, as described at http://www.bostonlightsource.com/content39128

### Setup of microcontroller ###

* Download Raspbian image with OLA added from http://dl.openlighting.org/ Used raspbian-ola-0.9.5.zip
* Power up RPi with USB cable and wall wart.
* Connect to RPi using Putty on COM4 at 115200 bps or `screen /dev/tty.usbserialaskjfhaskjh 115200` Physical connection is with a USB cable to a FTDI breakout board to wires to pins 6, 8, 10 on RPi header.
* Username is pi; default password is openlighting

### Update stuff ###

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install avahi-daemon # for hostname.local name resolution

Change hostname to `colorcommons`

    sudo vim /etc/hostname

### Install Flask and uWSGI ###

    sudo apt-get install python-flask python-pip python-dev python-webcolors
    sudo pip install uwsgi # Have to install via pip because Debian version is old (1.2.3)

### Install autossh ###

    sudo apt-get install autossh

Copy over autossh-tunnel.conf

Run once: `ssh-keygen`

Append `/root/.ssh/id_rsa.pub` to rascalmicro.com, `/home/sms/.ssh/authorized_keys`

Ensure that in /etc/ssh/sshd_config, we have: `GatewayPorts yes`

Useful debugging commands

    netstat -lptu
    nc -v rascalmicro.com 12345 (tries to open TCP connection, which is first step of HTTP POST)

### Configure OLA ###


    sudo adduser pi olad

Log out and back in again.

    sh /usr/bin/ola_conf_plugins.sh status all
    sh /usr/bin/ola_conf_plugins.sh disable all
    sh /usr/bin/ola_conf_plugins.sh status all

Verify that the plugins are all disabled. Then edit `/var/lib/ola/conf/ola-uartdmx.conf` to set `enable = true` and set `device = /dev/ttyAMA0`

`sudo raspi-config` > Advanced Options > Serial to disable serial console on UART.

Reboot. If needed, you can also restart OLA using `sudo service olad restart` and see the startup log with `tail -n 100 /var/log/syslog`
