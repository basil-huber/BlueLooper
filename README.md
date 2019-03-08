
# Installation
## Requirements:
* Ubuntu 16
* Python3 with Pip
* Sooperlooper
* Liblo development files
* Jackd audio server

## Procedure
Use the following to install on ubuntu 16:
```
sudo apt-get install python3
sudo apt-get install python3-dev
sudo apt-get install libgtk2.0-dev
sudo apt-get install sooperlooper
sudo apt-get install liblo-dev
sudo apt-get install jackd
```

Then install the package using
```
pip install git+https://github.com/basil-huber/BlueLooper.git
```

# Usage
Just launch the following command to start all programs:
```
bluelooper
```
You might have to use `sudo`

# Troubleshooting
## Connecting to pedal
To see if your computer finds your pedal, use
```
sudo hcitool lescan
```
This should give you a list of discovered BLE(Bluetooth Lowenergy) devices.
There should be an entry for the pedal with the name `BLUE_PEDAL`