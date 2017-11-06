# Pawn Shy

![Pawn Shy](/Pictures/PawnShy1.jpg)

This is my entry to the Have I Been Pwned API competition.

Based on the fair ground game Coconut shy. The aim is to knock out as many pawns as possible using either your email address or website that hasn't been pwned (good luck with that!).

## Videos:

[Part 1](https://youtu.be/ber4mi4SVx4)

[Part 2](https://youtu.be/kG7oJAG3vGs)


The game is intended to be easy to play, for example, at a conference, and to give the player a fun visual indication, and to drive their interest in Have I Been Pwned.

When attending Signal London recently I noticed the attendee name badges were actually NFC cards, this could be used either to lookup the attendees email (or hash) or have the email/hash directly in the NFC card.

Whilst the Signal NFC cards didn't actually include my email address it would have been easy for Twilio to add a VCard for me, or a hash of my email to facilitate this game.

Likewise, many door entry systems use NFC or RFID cards. These cards could be linked to an email address through an external database and provide a simple and fun way for employees to check if their email has been pwned.

## How It's Made

* Raspberry Pi running Raspbian
* I actually used the OctoPi 0.14 image for this. (It isn't required, but it makes it easy to start the Pi headless and I had other reasons as well)
* NFC sensor (Micro NFC Board - https://www.seeedstudio.com/Micro-NFC-Board-p-2431.html)
* 5 LED Neopixel strip (https://www.adafruit.com/product/1376)
* 3D Printed case
* 3D (SLA) printed pawns

The Raspberry Pi polls the NFC sensor waiting for a card or p2p connection and reads the following to get an email/website:

* Card serial number - linked though an external database to email address
* Uri NDEF record for a website
* VCard NDEF record for email address (Not implemented)
* P2P uri send for a website

Once the Pi picks up an email or website the Have I Been Pwned API is queried to get either:

* the number of times the email appears in a pwned site or 
* the number of accounts compromised for the website.

This is then displayed through the 5 pixel NeoPixel LEDs.

* As 0-5 Red/Purple vs Green/Yellow colouring for the count
* A sliding scale (1-100k, <1M, <10M, <100M, Wooo) of red/purple pwns indicting the number of accounts compromised.

Colours: typically Red for a compromise or Green when not used. However if using Minion pawns then Purple (bad minion) or Yellow (good minion/banana).

The LEDs are placed under the pawns and hidden from sight so it looks like the pawns are glowing.

Optional: A printer could be connected which prints out details of the compromise to allow the user to read up further.

## Games:

### Game 1: Have I Been Pwned

The aim of this game is to use your email address and make all the pawns go green (or yellow for Minion pawns).

Present a NFC card that either includes your email address, a hash or the id is linked to a database or email addresses (e.g. a door key)

Each red (or purple minion) pawn indicates the count of compromised sites the email is associated with.


### Game 2: Have They Been Pwned

The aim of this game is to find the website that has not been pwned, or in multi-player mode, to find the website with the lowest pwnage.

Using pre-programmed NFC cards, select a card for the website you trust the most. Present the the Game Of Pwned sensor.

Each red/purple pwnd indicates a pwnage.
0: Yay, not pwned!
1: 1-100k accounts compromised.
2: <1M
3: <10M
4: <100M
5: OUCH!

For multi-player you each select a card and the winner is the person with the lowest pwnage.


### Game 3: Send in the pwnage (Android Only)

Like game 2, the aim of this game is to find your favorite website without pwnage.

Ensure NFC Android Beam is enabled on your phone.

Browse to a website you trust (or don't!) and have an account with.

Place your phone on the Game Of Pwned.

When promoted by your phone click to send the website.

As with game 2. The pwnd accounts are displayed.


## Construction

### NeoPixels

Neopixels need to be driven with a serial data signal 70% of the power supply, and can work from a 3.6-5V Power supply. Sadly the Pi uses 3v3 for it's signals so the 3v3 power will not power the neopixels so our only choice is to use the 5V power. This then means that the 3v3 DIn will not be within the 70% required value. So we use a small diode inline with the 5V supply to drop it down to 4V4, brining our 3v3 signal to 75% of the power signal. With only 5 LEDs being driven the current draw should be low (300mA max) so a IN4001 diode will be more than sufficient.

* Cut a Neopixel strip to 5 LEDs along the cut line shown on the taps.
* Connect 3 wires to the input (5V/DIn/Gnd) side of the Neopixel strip.
* Connect a IN4001 diode in the 5V line with the current flow going towards the LEDs (diode band nearest the LEDs). Connect the other end of the diode to the 5V Pin.
* Connect a 300-600 Ohm resistor to the Din wire (to limit the current and protect the LEDs). Connect the other end of this to Pin 12 on the Pi).
* Connect Gnd straight to the Pi.

Note that Neopixels are not really a good choice for use on the Raspberry Pi. 

Install the raspberry Pi Neopixel software following the instructions here:

https://learn.adafruit.com/neopixels-on-raspberry-pi/software

![Neopixel Wiring](/Pictures/Wiring.jpg)

![Neopixel To Pi](/Pictures/NeopixelToPi.jpg)

## Pi

Ensure Neopixel LEDs connected as:

* Pin 2 = +5V
* Pin 6 = GND
* Pin 12 = DIn

Connect a USB power cable to the Pi before mounting (You might not be able to plug into the Pi once mounted).

Ensure your SD card in the Pi is working.

Mount the pi inside on the back wall. Use four M2.5 x6mm machine screws from the back into M2.5 x 11mm standoffs (Farnell 294583) which the Pi is mounted to, then M2.5 nuts on the other side of the Pi to secure it.

## NFC reader

If you're using M3 heat fit inserts to bold the holder to the case fit these with a hot soldering iron. Ensure that that are facing the correct way (fat end up with the large open area of the holder up as well).

Using a Micro NFC Board place this in the 3D printed holder with the component side of the PCB facing down into the holder so the blank side will sit against the inside of the case.

Fit the USB lead to the NFB board.

Screw the holder to the inside of the case. It doesn't quite fit in the center due to the USB connector, so it's pushed to one side.

Plug the USB lead into the Raspberry Pi.

![NFC Holder](/Pictures/NfcHolder.jpg)

![Mounting the NFC Holder](/Pictures/MountingNfcHolder.jpg)

![Inside Pawn Shy](/Pictures/InsidePawnShy.jpg)


## Pawns:

The pawns are 3D Printed (I used a Form2 with clear resin as this gives a nice print). 

Various Pawn models are available:

* Eureka Pawn: https://www.thingiverse.com/thing:173436
* Bender Bust: https://www.thingiverse.com/thing:182789
* Bender Can Holder: http://www.thingiverse.com/thing:1513101
* Minions: https://www.thingiverse.com/thing:376059

The models should be resized to about 26mm on the x/y axis to fit the stand.

Eureka Pawn and Bender are also available in the Pawns folder as hollowed out versions which might work better for FDM printers with clear filament.

![Alternative Pawns](/Pictures/AlternativePawns.jpg)

### Printer Settings:

* Printer: Form2
* Resing: Clear (V2)
* Layer height: 0.1mm
* Placement: Manually placed to ensure supports are on the back/bottom.
* Supports: auto-generated

### Bluetooth printer notes:

Not implemented but a Bluetooth printer could be used to print out the pwned details.

https://www.cnet.com/uk/how-to/how-to-setup-bluetooth-on-a-raspberry-pi-3/

http://mattrichardson.com/Raspberry-Pi-Wireless-Photo-Printing/index.html