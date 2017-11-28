Deployed version as of June 5, 2017 is:
    pi@colorcommons ~/color-commons $ git log
    commit 3aae3d47dc2331b2ea7a52fd0e9325d2c3816e7a
    Author: Brandon Stafford <brandon@pingswept.org>
    Date:   Mon Jun 5 16:15:27 2017 -0400
        Add flip code

A few customizations made on site:

    pi@colorcommons ~/color-commons $ git diff
    diff --git a/autossh.conf b/autossh.conf
    index 6fa117e..b872734 100644
    --- a/autossh.conf
    +++ b/autossh.conf
    @@ -3,7 +3,7 @@
     ; copy this file to /etc/supervisor/conf.d/autossh.conf
     ; check status with: supervisorctl status autossh
     [program:autossh]
    -command=autossh -i /home/pi/.ssh/id_rsa -M 12300 -R *:12345:localhost:8080 sms@45.33.87.121 -N
    +command=autossh -i /home/pi/.ssh/id_rsa -M 12300 -R *:12345:localhost:8080 -R *:22345:localhost:22 sms@45.33.87.121 -N
     user=pi
     autorestart=true
     startretries=100
    diff --git a/server.py b/server.py
    index e3a6132..be1cabe 100644
    --- a/server.py
    +++ b/server.py
    @@ -110,7 +110,7 @@ def parse_sms():
             data.append(color[2])
             data = data * num_fixtures

    -    ip = "172.16.11.50"
    +    ip = "192.168.95.105"
         port = 5000
         message = "listentome"
         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Updating IP address to target with sACN packets to 192.168.95.29 on November 28, 2017.
