# Using the Micro NFC Board Reader

Update firmware following instructions from: https://github.com/AppNearMe/micronfcboard-python

(Note: I used windows, the USB bulk storage worked nicely).


 
Install Libusb: https://askubuntu.com/questions/629619/how-to-install-libusb

$ sudo apt-get install libusb-1.0-0-dev

$ sudo apt-get install libusb-1.0-21-dev

Pi might already have this installed.

$ ldconfig -p | grep libusb 


https://github.com/walac/pyusb

(Starting with OctoPi 0.14)

Install Pip:
sudo apt-get install python-pip

Install PyUSB:

$ sudo pip install pyusb


// Get the examples.
git clone https://github.com/AppNearMe/micronfcboard-python.git

run blink example to check for working connection to the board.

needed to be run as sudo.

$ sudo python blink.py

------------------
Access to USB:
Id: 1fc9:8039

// Create the rules file
sudo nano /etc/udev/rules.d/99-local.rules

// Add
SUBSYSTEM=="usb", ATTRS{idVendor}=="1fc9", MODE="0666"

// reload (remove USB device as well)
udevadm control --reload-rules

------------------

$ python blink.py


--------------------------------
Bluetooth (Printer)
