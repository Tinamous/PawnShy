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
					self.do_ndef_web_lookup(uid, ndef_record)
				elif isinstance(ndef_record, MIMERecord):
					self.do_ndef_email_lookup(uid, ndef_record)
				else:
					print("Don't know how to handle ndef record. reverting to card id.")
					self.do_card_id_lookup(uid)

			# Sleep for a bit to show the result then return to not busy led animation
			time.sleep(20)
			self.led_driver.animate_whilst_not_busy()

	# Expect ndef to be MIMERecord
	# and the MIMERecord to be a vcard
	def do_ndef_email_lookup(self, uid, ndef_record):
		print("Email lookup. Mime type:")
		print (ndef_record.mimeType)
		print("Email lookup. Data:")
		print (ndef_record.data)

		self.do_email_lookup("Test@domain.com")

	def do_email_lookup(self, email):

		self.led_driver.animate_whilst_hibp_lookup()
		count, results = self.hibp_lookup.lookup_email(email)

		# Ignore the results for now but we might want to print them
		# for the person to take away.

		# Show the pwn count.
		self.led_driver.show_result_email_count(count)

	# Expect URIRecord
	def do_ndef_web_lookup(self, uid, ndef_record):
		print("Web address lookup")
		uri = ndef_record.uri
		print(uri)

		print("Extract domain")
		parsed_uri = urlparse(uri)
		domain = '{uri.netloc}'.format(uri=parsed_uri)
		print ("'" + domain + "'")

		# Bodge warning!
		# TODO: If uri starts with "http://mobile.board.net" it's the Signal NFC
		# namebadge. Use card id lookup instead
		if domain == "mobile.bcard.net":
			return self.do_card_id_lookup(uid)

		self.do_web_lookup(domain)

	def do_web_lookup(self, domain):

		self.led_driver.animate_whilst_hibp_lookup()
		count, results = self.hibp_lookup.lookup_domain(domain)

		# Ignore the results for now but we might want to print them
		# for the person to take away.

		# Show the pwn count.
		self.led_driver.show_result_web_count(count)


	def do_card_id_lookup(self, card_id):
		print("Card id lookup")
		# Total hack...
		# Use card UID to lookup against a known database
		# for the email address.
		# Or for non-programmable cards, use the id for domain lookup.
		if card_id == "0430ACD2865880":
			print("Steves Signal card")
			self.do_email_lookup("Stephen.Harrison@AnalysisUK.com")
		elif card_id == "62EB23EE":
			print("Tesco.com blank rfid card")
			self.do_web_lookup("Tesco.com")
		else:
			print("Unknown card")

# Main program logic follows:
if __name__ == '__main__':
	app = App()
	app.start()