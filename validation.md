What the NJ server looks like when it's functional:

    root@debian:~# netstat -plnt
    Active Internet connections (only servers)
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
    tcp        0      0 0.0.0.0:12345           0.0.0.0:*               LISTEN      27273/sshd: sms
    tcp        0      0 0.0.0.0:22345           0.0.0.0:*               LISTEN      27273/sshd: sms
    tcp        0      0 0.0.0.0:12300           0.0.0.0:*               LISTEN      27273/sshd: sms
    tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      3685/sshd
    tcp6       0      0 :::12345                :::*                    LISTEN      27273/sshd: sms
    tcp6       0      0 :::22345                :::*                    LISTEN      27273/sshd: sms
    tcp6       0      0 :::12300                :::*                    LISTEN      27273/sshd: sms
    tcp6       0      0 :::22                   :::*                    LISTEN      3685/sshd
    root@debian:~# ifconfig
    eth0      Link encap:Ethernet  HWaddr f2:3c:91:e7:d9:89
              inet addr:45.33.87.121  Bcast:45.33.87.255  Mask:255.255.255.0
              inet6 addr: 2600:3c03::f03c:91ff:fee7:d989/64 Scope:Global
              inet6 addr: fe80::f03c:91ff:fee7:d989/64 Scope:Link
              UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
              RX packets:29636410 errors:0 dropped:0 overruns:0 frame:0
              TX packets:27919325 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000
              RX bytes:3943248315 (3.6 GiB)  TX bytes:4790941295 (4.4 GiB)
