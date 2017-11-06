from hibpLookup import HibpLookup
from ledDriver import LedDriver
from nfcReader import NfcReader
from cardIdLookup import CardIdLookup

import time
from micronfcboard.board import MicroNFCBoard
from micronfcboard.nfc.ndef import URIRecord, TextRecord, SmartPosterRecord, MIMERecord
from urlparse import urlparse

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

			if not ndef_record:
				self.do_card_id_lookup(uid)
			else:
				if isinstance(ndef_record, URIRecord): # - website. (if starts with http or https. Also check email:
					self.do_web_lookup(uid, ndef_record)
				elif isinstance(ndef_record, MIMERecord):
					self.do_email_lookup(uid, ndef_record)
				else:
					print("Don't know how to handle ndef record. reverting to card id.")
					self.do_card_id_lookup(uid)

			time.sleep(0.1)

	# Expect ndef to be MIMERecord
	# and the MIMERecord to be a vcard
	def do_email_lookup(self, uid, ndef_record):
		print("Email lookup. Mime type:")
		print (ndef_record.mimeType)
		print("Email lookup. Data:")
		print (ndef_record.data)

		self.led_driver.animate_whilst_hibp_lookup()
		count = self.hibp_lookup.lookup_email("Test@domain.com")
		# Insert artificial delay to make it look pretty...
		time.sleep(5)
		# Show the pwn count.
		self.led_driver.show_result_email_count(count)
		# Sleep for 5 seconds.
		time.sleep(20)
		self.led_driver.animate_whilst_not_busy()

	# Expect URIRecord
	def do_web_lookup(self, uid, ndef_record):
		print("Web address lookup")
		uri = ndef_record.uri
		print(uri)

		parsed_uri = urlparse(uri)
		domain = '{uri.netloc}'.format(uri=parsed_uri)
		print domain

		self.hibp_lookup.lookup_domain(domain)

		# Bodge warning!
		# TODO: If uri starts with "http://mobile.board.net" it's the Signal NFC
	    # namebadge. Use card id lookup instead


	def do_card_id_lookup(self, card_id):
		print("Card id lookup")


# Main program logic follows:
if __name__ == '__main__':
	app = App()
	app.start()