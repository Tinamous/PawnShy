# Mainly copied from NeoPixel strandtest example. Author: Tony DiCola (tony@tonydicola.com)
# See: https://github.com/jgarff/rpi_ws281x

import time

from neopixel import *

# Led Driver for Pawn Shy to animate / set the Pawn LED states.
class LedDriver():

	def __init__(self):
		# LED strip configuration:
		LED_COUNT      = 5      # Number of LED pixels.
		LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
		LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
		LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
		LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
		LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
		LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
		LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

		# Create NeoPixel object with appropriate configuration.
		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

		# Intialize the library (must be called once before other functions).
		strip.begin()

	# Animate the LEDs whilst we wait for a user input
	def animate_whilst_not_busy(self):
		theaterChase(self.strip, Color(127, 0, 0))  # Red theater chase
		theaterChase(self.strip, Color(0, 0, 127))  # Blue theater chase
		theaterChase(self.strip, Color(0, 127, 0))  # Blue theater chase

	# Animate the LEDs whilst the HIBP result is being retreived
	def animate(self):
		print ('Color wipe animation red.')
		self.colorWipe(self.strip, Color(255, 0, 0))  # Red wipe
		self.bad_color = Color(128, 0, 0)
		self.good_color = Color(0, 0, 0)

		#print ('Color wipe animation blue.')
		#colorWipe(strip, Color(0, 255, 0))  # Blue wipe

		#print ('Color wipe animation green')
		#colorWipe(strip, Color(0, 0, 255))  # Green wipe

		#print ('Theater chase animations.')
		#theaterChase(strip, Color(127, 127, 127))  # White theater chase
		#theaterChase(strip, Color(127, 0, 0))  # Red theater chase
		#theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
		#print ('Rainbow animations.')
		#rainbow(strip)
		#rainbowCycle(strip)
		#theaterChaseRainbow(strip)


	def show_result_count(self, count):
		# TODO: Animate a little as we go.
		# Yay, no pwn, show nothing
		for i in range(self.strip.numPixels()):
			if i < count:
				self.strip.setPixelColor(i, self.good_color)
			else:
				# Purple
				self.strip.setPixelColor(i, self.bad_color)
			self.strip.show()

	def show_result_pwn_count(self, count):

		# TODO: Animate a little as we go along.

		if count < 1:
			# Yay, no pwn, show nothing
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, self.good_color)
				self.strip.show()
		elif count < 1000:
			self.strip.setPixelColor(1, self.good_color)
			self.strip.setPixelColor(2, self.good_color)
			self.strip.setPixelColor(3, self.good_color)
			self.strip.setPixelColor(4, self.good_color)
			self.strip.setPixelColor(5, self.bad_color)
		elif count < 10000:
			self.strip.setPixelColor(1, self.good_color)
			self.strip.setPixelColor(2, self.good_color)
			self.strip.setPixelColor(3, self.good_color)
			self.strip.setPixelColor(4, self.bad_color)
			self.strip.setPixelColor(5, self.bad_color)
		elif count < 100000:
			self.strip.setPixelColor(1, self.good_color)
			self.strip.setPixelColor(2, self.good_color)
			self.strip.setPixelColor(3, self.bad_color)
			self.strip.setPixelColor(4, self.bad_color)
			self.strip.setPixelColor(5, self.bad_color)
		elif count < 1000000:
			self.strip.setPixelColor(1, self.good_color)
			self.strip.setPixelColor(2, self.bad_color)
			self.strip.setPixelColor(3, self.bad_color)
			self.strip.setPixelColor(4, self.bad_color)
			self.strip.setPixelColor(5, self.bad_color)
		else:
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, Color(255,0,0))
				self.strip.show()

	# Define functions which animate LEDs in various ways.
	def colorWipe(self, strip, color, wait_ms=50):
		"""Wipe color across display a pixel at a time."""
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, color)
			strip.show()
			time.sleep(wait_ms / 1000.0)

	def theaterChase(self, strip, color, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		for j in range(iterations):
			for q in range(3):
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i + q, color)
				strip.show()
				time.sleep(wait_ms / 1000.0)
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i + q, 0)

	def wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def rainbow(self, strip, wait_ms=20, iterations=1):
		"""Draw rainbow that fades across all pixels at once."""
		for j in range(256 * iterations):
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, self.wheel((i + j) & 255))
			strip.show()
			time.sleep(wait_ms / 1000.0)

	def rainbowCycle(self, strip, wait_ms=20, iterations=5):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		for j in range(256 * iterations):
			for i in range(strip.numPixels()):
				strip.setPixelColor(i, self.wheel((int(i * 256 / strip.numPixels()) + j) & 255))
			strip.show()
			time.sleep(wait_ms / 1000.0)

	def theaterChaseRainbow(self, strip, wait_ms=50):
		"""Rainbow movie theater light style chaser animation."""
		for j in range(256):
			for q in range(3):
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i + q, self.wheel((i + j) % 255))
				strip.show()
				time.sleep(wait_ms / 1000.0)
				for i in range(0, strip.numPixels(), 3):
					strip.setPixelColor(i + q, 0)

# Main program logic follows:
if __name__ == '__main__':
	driver = LedDriver();
	driver.animate();




