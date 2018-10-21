RPi setup:
- `sudo raspi-config` in terminal
enable uart
disable serial login
enable uart hardware


Running python3.6 programs:
- install python 3.6 (follow instructions online)

- pip3.6 install <all dependencies>
(includes pyserial, pycrypto, and ML libraries)

- to run python3.6 scripts, use `python3.6 <name>.py`


wireless RPi setup:
- connect pi to hotspot for the first time (requires monitor)

- subsequently, the pi will automatically connect to hotspot upon boot

- find IP address of pi by looking at connected devices on phone's hotspot GUI

- ssh or vnc to pi using laptop using the pi's IP address




