
## Raspberry Pi Setup
Install pigpio
```
sudo apt update
sudo apt install pigpio
```
Configure it to run as a service
1. Create a file in `/etc/systemd/system/` with the contets
```
[Unit]
Description=Pigpio daemon
After=network.target syslog.target
StartLimitIntervalSec=60
StartLimitBurst=5
StartLimitAction=reboot

[Service]
Type=simple
ExecStart=/usr/bin/pigpiod -g -s 2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
2. Enable the service `sudo systemctl enable pigpiod.service`
3. Start the service `sudo systemctl start pigpiod.service`
