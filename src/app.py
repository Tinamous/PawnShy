from .hibpLookup import HibpLookup
from .ledDriver import LedDriver
from .nfcReader import NfcReader
from .cardIdLookup import CardIdLookup

import time

class App():
	def __init__(self):
		print("Pawn Shy application init...")
		self.hibp_lookup = HibpLookup()
		self.nfc_reader = NfcReader()
		self.card_id_lookup = CardIdLookup()
		self.led_driver = LedDriver()

	def start(self):
		print("Running Pawn Shy application. Press Ctrl-C to quit")

		self.led_driver.start()

		while True:
			uid, ndef_record = self.nfc_reader.poll_for_card()

			print ("Card reader poll result:")
			print uid
			print ndef_record

			# TODO: If...
			# isinstance(ndef_record, URIRecord) - website. (if starts with http or https. Also check email:
			# isinstance(ndef_record, TextRecord) - ?? - see if email
			# isinstance(ndef_record, MIMERecord) - vcard.
			if ndef_record:
				self.do_email_lookup(ndef_record)

			time.sleep(0.1)

	def do_email_lookup(self, ndef):
		print("Email lookup")
		self.led_driver.animate_whilst_hibp_lookup()
		count = self.hibp_lookup.lookup_email("Test@domain.com")
		# Insert artificial delay to make it look pretty...
		time.sleep(5)
		# Show the pwn count.
		self.led_driver.show_result_email_count(count)
		# Sleep for 5 seconds.
		time.sleep(5)
		self.led_driver.animate_whilst_not_busy()

	def do_web_lookup(self, ndef):
		print("Web address lookup")

	def do_card_id(self, card_id):
		print("Card id lookup")


# Main program logic follows:
if __name__ == '__main__':
	app = App()
	app.start()