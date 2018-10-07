
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
sudo apt-get install sooperlooper
sudo apt-get install liblo-dev
sudo apt-get install jackd
```

Then install the package using
```
pip install ...
```

# Usage
The configuration 

Start a jackd server with your recording and playback device:
```jackd -d alsa -P hw:Amplifier -C hw:Amplifier & ```

Start sooperlooper:
```sooperlooper -q &```

Connect your recording and playback devices to sooperlooper:
```
jack_connect system:capture_1 sooperlooper:common_in_1
jack_connect system:capture_2 sooperlooper:common_in_2
jack_connect sooperlooper:common_out_1 system:playback_1
jack_connect sooperlooper:common_out_2 system:playback_2
```


Start the sooperlooper gui:
```
slgui &
```

Then start the python application that connects the pedal to sooperlooper as super user

# Troubleshooting
## Connecting to pedal
To see if your computer finds your pedal, use
```
sudo hcitool lescan
```
This should give you a list of discovered BLE(Bluetooth Lowenergy) devices.
There should be an entry for the pedal with the name `BLUE_PEDAL`