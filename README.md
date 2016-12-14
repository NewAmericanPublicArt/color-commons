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

Probably healthy spew from OLA:

    Dec 14 10:38:25 colorcommons olad: olad/Olad.cpp:94: OLA Daemon version 0.9.5
    Dec 14 10:38:25 colorcommons olad: olad/OlaDaemon.cpp:97: Using configs in /var/lib/ola/conf
    Dec 14 10:38:25 colorcommons olad: common/thread/Thread.cpp:190: Thread pref-saver, policy SCHED_OTHER, priority 0
    Dec 14 10:38:25 colorcommons olad: olad/OlaServer.cpp:190: Server UID is 7a70:f00a10ac
    Dec 14 10:38:25 colorcommons olad: olad/OlaServer.cpp:202: Server instance name is OLA Server
    Dec 14 10:38:25 colorcommons olad: olad/Preferences.cpp:408: Missing /var/lib/ola/conf/ola-universe.conf: No such file or directory - this isn't an error, we'll just use the defaults
    Dec 14 10:38:25 colorcommons olad: olad/AvahiDiscoveryAgent.cpp:201: Client state changed to AVAHI_CLIENT_S_RUNNING
    Dec 14 10:38:25 colorcommons olad: common/thread/Thread.cpp:190: Thread http, policy SCHED_OTHER, priority 0
    Dec 14 10:38:25 colorcommons olad: common/http/HTTPServer.cpp:490: HTTP Server started on port 9090
    Dec 14 10:38:25 colorcommons olad: olad/AvahiDiscoveryAgent.cpp:236: State for OLA Server._http._tcp,_ola, group 0xd2d7e0 changed to AVAHI_ENTRY_GROUP_UNCOMMITED
    Dec 14 10:38:25 colorcommons olad: olad/AvahiDiscoveryAgent.cpp:334: Adding _ola._sub._http._tcp
    Dec 14 10:38:25 colorcommons olad: olad/AvahiDiscoveryAgent.cpp:342: Failed to add _ola._sub._http._tcp
    Dec 14 10:38:25 colorcommons olad: olad/OlaServer.cpp:473: Updated PID definitions.
    Dec 14 10:38:25 colorcommons olad: olad/AvahiDiscoveryAgent.cpp:236: State for OLA Server._http._tcp,_ola, group 0xd2d7e0 changed to AVAHI_ENTRY_GROUP_REGISTERING
    Dec 14 10:38:25 colorcommons olad: olad/OlaServer.cpp:481: pid store is at 0xd9abd8
    Dec 14 10:38:25 colorcommons olad: common/thread/Thread.cpp:190: Thread signal-thread, policy SCHED_OTHER, priority 0
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping ArtNet because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping Dummy because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping E1.31 (sACN) because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping ESP Net because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping GPIO because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping KarateLight because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping KiNET because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping Milford Instruments because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping Enttec Open DMX because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping Open Pixel Control because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping OSC because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping Renard because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping SandNet because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping ShowNet because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping SPI because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping StageProfi because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping Serial USB because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping USB because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping Pathport because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:73: Skipping FTDI USB DMX because it was disabled
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:104: Trying to start UART native DMX
    Dec 14 10:38:25 colorcommons olad: common/io/ExtendedSerial.cpp:69: Port speeds for 22 are 250000 in and 250000 out
    Dec 14 10:38:25 colorcommons olad: common/thread/Thread.cpp:190: Thread , policy SCHED_OTHER, priority 0
    Dec 14 10:38:25 colorcommons olad: olad/DeviceManager.cpp:105: Installed device: UART native DMX:20-/dev/ttyAMA0
    Dec 14 10:38:25 colorcommons olad: olad/PluginManager.cpp:108: Started UART native DMX
    Dec 14 10:38:25 colorcommons olad: plugins/uartdmx/UartDmxThread.cpp:136: Granularity for UART thread is GOOD
    Dec 14 10:38:25 colorcommons kernel: [  599.044667] uart-pl011 3f201000.uart: no DMA platform data
    Dec 14 10:38:26 colorcommons olad: olad/AvahiDiscoveryAgent.cpp:236: State for OLA Server._http._tcp,_ola, group 0xd2d7e0 changed to AVAHI_ENTRY_GROUP_ESTABLISHED

To configure pin 18 on the RPi to go high at boot, which puts the Bitwizard DMX shield into output mode, copy the file `set_dmx_mode` from this repo to `/usr/bin/set_dmx_mode` and make it executable with `sudo chmod 755 /usr/bin/set_dmx_mode`

Then execute that file at boot by putting this line in `/etc/rc.local` somewhere before the line `exit 0`


