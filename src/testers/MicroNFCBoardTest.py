# Based on examples from AppNearMe Micro NFC Board Python API.
# See: https://github.com/AppNearMe/micronfcboard-python

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from time import sleep
from micronfcboard.board import MicroNFCBoard

def read_from_nfc(board):

    print("Polling...")
    while board.polling:
        sleep(0.1)

    if board.connected:
        print("Connected")
    else:
        print("Not connected")
        exit()

    if board.p2p:
        handle_p2p(board)
    elif board.type2Tag:
        handle_tag(board)
    else:
        print("Unknown board condition")

def handle_p2p(board):
    print("P2P mode")

    ndefMessageRead = False
    if not ndefMessageRead and board.ndefPresent:
        print("Received:")
        ndefMessageRead = True
        for record in board.ndefRecords:
            print record
    sleep(0.1)

def handle_tag(board):
    print("Tag!")
    atqa, sak, uid = board.getNfcInfo()
    print("ISO A tag detected: ATQA: %s, SAK: %s, UID %s" % (atqa, sak, uid,))

    ndefMessageRead = False
    ndefReadingStarted = False

    if not ndefReadingStarted and board.ndefReadable:
        print("Reading tag")
        ndefReadingStarted = True
        board.ndefRead()
    if not ndefMessageRead and board.ndefPresent:
        print("Message read:")
        ndefMessageRead = True
        for record in board.ndefRecords:
            print record
    sleep(0.1)

	
board = MicroNFCBoard.getBoard()

if( board == None ):
    print("Board not found")
    exit()

board.open()

print("Connected to board id %s (version %d.%d)" % (board.id, board.version[0], board.version[1]) )

if not board.connected:
    print("Start polling")
    board.startPolling(True, False, True)

try:
    while True:
        read_from_nfc(board)
except KeyboardInterrupt:
    pass

print ("Disconnected")
board.close()
exit()

