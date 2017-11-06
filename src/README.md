# Pawn Shy Software

Written in Python 2.7.

Needs MicroNFCBoard, this is directly copied into the file structure from AppNearMe git repository.

Install the raspberry Pi Neopixel software following the instructions here:

https://learn.adafruit.com/neopixels-on-raspberry-pi/software

## Files

* app.py - the main application. run this using: $ sudo python app.py
* cardIdLookup.py - intended to do card serial number to email/domain. Unused at present
* hibpLookup.py - responsible for getting the count for pwned emails/accounts/domains from HaveIBeenPwned.com
* ledDriver.py - responsible for driving the LED (pawn) display
* nfcReader - interfaces to the NFC board to read tags or p2p connections.
* testers/MicroNFCBoardTest.py - this script connects to the MicroNFCBoard and watches for either a P2P connection or a tag
* testers/Neopixels.py - test for the Neopixel driver

## Run the application.

* clone this repository
* ensure you've set-up the NFC and NeoPixel libraries as described in the main readme
* open the .src folder
* use 
** sudo python app.py 