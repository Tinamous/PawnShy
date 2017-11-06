
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from time import sleep
from micronfcboard.board import MicroNFCBoard

class NfcReader():

	def __init__(self):
		print("Connecting to NFC board")

		self.board = MicroNFCBoard.getBoard()

		if (self.board == None):
			print("NFC Board not found. Unable to continue")
			exit()

		self.board.open()

		print("Connected to board id %s (version %d.%d)" % (self.board.id, self.board.version[0], self.board.version[1]))

	# returns tuple of card uid and first ndef record found.
	def poll_for_card(self):
		print("Polling...")

		if not self.board.connected:
			print("Start polling")
			self.board.startPolling(True, False, True)

		while self.board.polling:
			sleep(0.1)

		if self.board.connected:
			print("Connected")
		else:
			return None,None

		if self.board.p2p:
			return self.handle_p2p(self.board)
		elif self.board.type2Tag:
			return self.handle_tag(self.board)
		else:
			print("Unknown board condition")

		return

	# returns tuple of card uid and first ndef record found.
	def handle_p2p(self, board):
		print("P2P mode")

		if board.ndefPresent:
			print("Received p2p ndef record:")

			# HACK: return only the first.
			for record in board.ndefRecords:
				return "", record
		sleep(0.1)

	# returns tuple of card uid and first ndef record found.
	def handle_tag(self, board):
		print("Tag!")
		atqa, sak, uid = board.getNfcInfo()
		print("ISO A tag detected: ATQA: %s, SAK: %s, UID %s" % (atqa, sak, uid,))

		ndefMessageRead = False
		ndefReadingStarted = False

		while True:

			if board.ndefReadable:
				print("Reading tags ndef record")
				board.ndefRead()
			else:
				print("Tag not ndef readable")
				return uid, None

			if board.ndefPresent:
				print("ndef read.")

				# Hack return only the first.
				for record in board.ndefRecords:
					return uid, record

			# TODO: Add a timeout incase ndef read goes pairshaped.
			sleep(0.1)