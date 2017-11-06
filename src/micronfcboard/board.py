"""
MicroNFCBoard Python API

Copyright (c) 2014-2015 AppNearMe Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from array import array

from interface import INTERFACE, usb_backend
from transport import Transport

from nfc.ndef import URIRecord, TextRecord, SmartPosterRecord, MIMERecord

VID = 0x1FC9 #NXP VID
PID = 0x8039 #Attributed to AppNearMe

TARGET_FIRMWARE = (1, 4)

STATUS_POLLING        = (1 << 0)
STATUS_CONNECTED      = (1 << 1)
STATUS_NDEF_PRESENT   = (1 << 2)
STATUS_NDEF_READABLE  = (1 << 3)
STATUS_NDEF_WRITEABLE = (1 << 4)
STATUS_NDEF_BUSY      = (1 << 5)
STATUS_NDEF_SUCCESS   = (1 << 6)

STATUS_TYPE_MASK      = (0xFF << 8)
STATUS_TYPE1          = (1 << 8)
STATUS_TYPE2          = (2 << 8)
STATUS_TYPE3          = (3 << 8)
STATUS_TYPE4          = (4 << 8)
STATUS_P2P            = (8 << 8)

STATUS_INITIATOR      = (1 << 16)
STATUS_TARGET         = (0 << 16)

CHUNK_SIZE = 40

TEXT_ENCODING = {0: "utf-8", 1: "utf-16"}

class SmartPosterNestingException(Exception):
    pass

class FirmwareUpgradeRequiredException(Exception):
    pass

class MicroNFCBoard(object):
    @staticmethod
    def getBoard(number = 0):
        a = INTERFACE[usb_backend].getAllConnectedInterface(VID, PID)
        if((a != None) and (len(a) > number)):
            return MicroNFCBoard(a[number])
        return None
    
    @staticmethod
    def getAllBoards():
        return [MicroNFCBoard(i) for i in INTERFACE[usb_backend].getAllConnectedInterface(VID, PID)]
    
    def __init__(self, intf):
        self._intf = intf
        self._transport = Transport()
        self._id = None
        self._version = None
        self._polling = False
        self._connected = False
        self._type2 = False
        self._type4 = False
        self._p2p = False
        self._initiator = False
        self._ndefPresent = False
        self._ndefRecords = None
        self._ndefRead = False
        self._ndefReadable = False
        self._ndefWriteable = False
        self._ndefBusy = False
        self._ndefSuccess = False
        
    def open(self):
        self._transport.open(self._intf)
        version, revision, self._id = self._transport.info()
        self._version = (version, revision)
        if( self._version < TARGET_FIRMWARE ):
            #self._transport.reset(True)
            raise FirmwareUpgradeRequiredException("Your current firmware (version %d.%d) is outdated; please upgrade it to version %d.%d" % (version, revision, TARGET_FIRMWARE[0], TARGET_FIRMWARE[1]))
        
    def close(self):
        self._transport.close()
        
    @property
    def id(self):
        return self._id
    
    @property
    def connected(self):
        self._updateStatus()
        return self._connected

    @property
    def type2Tag(self):
        self._updateStatus()
        return self._type2 and self._initiator
    
    @property
    def type4Emulator(self):
        self._updateStatus()
        return self._type4 and not self._initiator
    
    @property
    def p2p(self):
        self._updateStatus()
        return self._p2p

    @property
    def polling(self):
        self._updateStatus()
        return self._polling
    
    @property
    def ndefReadable(self):
        self._updateStatus()
        return self._ndefReadable
    
    @property
    def ndefWriteable(self):
        self._updateStatus()
        return self._ndefWriteable
    
    @property
    def ndefPresent(self):
        self._updateStatus()
        return self._ndefPresent
    
    @property
    def ndefBusy(self):
        self._updateStatus()
        return self._ndefBusy
    
    @property
    def ndefSuccess(self):
        self._updateStatus()
        return self._ndefSuccess
    
    @property
    def ndefRecords(self):
        self._updateStatus()
        if self._ndefPresent and not self._ndefRead:
            self._ndefRecords = self._getNdefMessageRecords()
            self._ndefRead = True
        return self._ndefRecords
    
    @ndefRecords.setter
    def ndefRecords(self, records):
        self._updateStatus()
        self._ndefRecords = records
        #Push them to device
        self._setNdefRecords(self._ndefRecords)
    
    @property
    def version(self):
        return self._version
    
    def getNfcInfo(self):
        return self._transport.nfcGetInfo()
    
    def reset(self):
        self._transport.reset(False)
        
    def startPolling(self, readerWriter, emulator, p2p):
        self._transport.nfcPoll(readerWriter, emulator, p2p)
        
    def stopPolling(self):
        self._transport.nfcPoll(False, False, False)
        
    def ndefRead(self):
        self._transport.nfcOperation(True, False)
        
    def ndefWrite(self):
        self._transport.nfcOperation(False, True)
        
    def setLeds(self, led1, led2):
        self._transport.leds(led1, led2)
        
    def _updateStatus(self):
        status = self._transport.status()
        self._polling = (status & STATUS_POLLING) != 0
        self._connected = (status & STATUS_CONNECTED) != 0
        self._ndefPresent = (status & STATUS_NDEF_PRESENT) != 0
        self._ndefReadable = (status & STATUS_NDEF_READABLE) != 0
        self._ndefWriteable = (status & STATUS_NDEF_WRITEABLE) != 0
        self._ndefBusy = (status & STATUS_NDEF_BUSY) != 0
        self._ndefSuccess = (status & STATUS_NDEF_SUCCESS) != 0
        self._type2 = (status & STATUS_TYPE_MASK) == STATUS_TYPE2
        self._type4 = (status & STATUS_TYPE_MASK) == STATUS_TYPE4
        self._p2p = (status & STATUS_TYPE_MASK) == STATUS_P2P
        self._initiator = (status & STATUS_INITIATOR) != 0
        
        if not self._ndefPresent:
            self._ndefRead = False
            self._ndefRecords = None
        
    def _getNdefRecords(self, start, count):
        records = []
        for recordNumber in range(start, start+count):
            #Get records info
            recordType, recordInfo = self._transport.nfcGetRecordInfo(recordNumber)
            funcs = {   0 : self._parseUnknownRecord,
                        1 : self._parseURIRecord,
                        2 : self._parseTextRecord,
                        3 : self._parseSmartPosterRecord,
                        4 : self._parseMIMERecord,
                    }
            record = funcs[recordType](recordNumber, recordInfo)
            if record != None:
                records += [record]
        return records
    
    def _getNdefMessageRecords(self):    
        #Get message count
        recordsCount = self._transport.nfcGetMessageInfo()
        return self._getNdefRecords(0, recordsCount)
    
    def _parseUnknownRecord(self, recordNumber, recordInfo):
        return None
    
    def _parseURIRecord(self, recordNumber, recordInfo):
        uriPrefix = recordInfo[0]
        uriLength = recordInfo[1]
        uri = unicode(self._decodePrefix(uriPrefix).tostring() + self._getRecordData(recordNumber, 0, uriLength).tostring(), "utf-8")
        return URIRecord(uri)
    
    def _parseTextRecord(self, recordNumber, recordInfo):
        encoding = TEXT_ENCODING[recordInfo[0]]
        languageCodeLength = recordInfo[1]
        textLength = recordInfo[2]
        languageCode = unicode(self._getRecordData(recordNumber, 0, languageCodeLength).tostring(), "utf-8")
        text = unicode(self._getRecordData(recordNumber, 1, textLength).tostring(), encoding)
        return TextRecord(text, languageCode, encoding)
    
    def _parseSmartPosterRecord(self, recordNumber, recordInfo):
        recordsStart = recordInfo[0]
        recordsCount = recordInfo[1]
        records = self._getNdefRecords(recordsStart, recordsCount)
        return SmartPosterRecord(records)
    
    def _parseMIMERecord(self, recordNumber, recordInfo):
        mimeTypeLength = recordInfo[0]
        dataLength = recordInfo[1]
        mimeType = unicode(self._getRecordData(recordNumber, 0, mimeTypeLength).tostring(), "utf-8")
        data = self._getRecordData(recordNumber, 1, dataLength)
        return MIMERecord(mimeType, data)
    
    def _decodePrefix(self, prefix):
        return self._transport.nfcDecodePrefix(prefix)
    
    def _getRecordData(self, recordNumber, item, itemLength):
        buf = array("B")
        while len(buf) < itemLength:
            chunkLength = min(CHUNK_SIZE, itemLength - len(buf))
            buf += self._transport.nfcGetRecordData(recordNumber, item, len(buf), chunkLength)
        return buf
    
    def _setNdefRecords(self, records):
        self._transport.nfcPrepareMessage(True, False)
        recordNumber = 0
        spRecordNumber = len(records) #Smart poster records after main records
        for record in records:
            spRecordNumber = self._addNdefRecord(recordNumber, record, spRecordNumber)
            recordNumber += 1
        self._transport.nfcSetMessageInfo(recordNumber)
        self._transport.nfcPrepareMessage(False, True)
        recordNumber = 0
        spRecordNumber = len(records) 
        for record in records:
            spRecordNumber = self._setNdefRecord(recordNumber, record, spRecordNumber)
            recordNumber += 1
        #self._transport.nfcSetMessageInfo(recordNumber)
        
    def _addNdefRecord(self, recordNumber, record, recordsStart, spAllowed = True):
        funcs = {   URIRecord : self._generateURIRecord,
                    TextRecord : self._generateTextRecord,
                    SmartPosterRecord : self._generateSmartPosterRecord,
                    MIMERecord : self._generateMIMERecord,
                }
        
        if( not spAllowed and type(record) == SmartPosterRecord ):
            raise SmartPosterNestingException()
                
        return funcs[type(record)](recordNumber, record, recordsStart)
        
    def _generateURIRecord(self, recordNumber, record, spRecordNumber):
        #Try to get prefix
        buf = array("B")
        buf.fromstring(record.uri)
        prefix, length = self._encodePrefix(buf[0:36])
        
        self._transport.nfcSetRecordInfo(recordNumber, 1, [prefix, len(buf[length:])])
        
        return spRecordNumber
        
    def _generateTextRecord(self, recordNumber, record, spRecordNumber):
        languageCodeBuf = array("B")
        languageCodeBuf.fromstring(record.language)
       
        textBuf = array("B")
        textBuf.fromstring(record.text)
        
        self._transport.nfcSetRecordInfo(recordNumber, 2, [{v: k for k, v in TEXT_ENCODING.items()}[record.encoding], len(languageCodeBuf), len(textBuf)])
        
        return spRecordNumber
        
    def _generateSmartPosterRecord(self, recordNumber, record, recordsStart):
        self._transport.nfcSetRecordInfo(recordNumber, 3, [recordsStart, len(record.records)])
        spRecordNumber = recordsStart
        
        for spRecord in record.records:
            self._addNdefRecord(spRecordNumber, spRecord, 0, False) #No sub records
            spRecordNumber += 1
            
        return spRecordNumber
    
    def _generateMIMERecord(self, recordNumber, record, spRecordNumber):
        mimeTypeBuf = array("B")
        mimeTypeBuf.fromstring(record.mimeType)
       
        dataBuf = array("B", record.data)
        
        self._transport.nfcSetRecordInfo(recordNumber, 4, [len(mimeTypeBuf), len(dataBuf)])
        
        return spRecordNumber
    
    def _setNdefRecord(self, recordNumber, record, recordsStart, spAllowed = True):
        funcs = {   URIRecord : self._setURIRecord,
                    TextRecord : self._setTextRecord,
                    SmartPosterRecord : self._setSmartPosterRecord,
                    MIMERecord : self._setMIMERecord,
                }
        
        if( not spAllowed and type(record) == SmartPosterRecord ):
            raise SmartPosterNestingException()
                
        return funcs[type(record)](recordNumber, record, recordsStart)
        
    def _setURIRecord(self, recordNumber, record, spRecordNumber):
        #Try to get prefix
        buf = array("B")
        buf.fromstring(record.uri)
        prefix, length = self._encodePrefix(buf[0:36])
        
        self._setRecordData(recordNumber, 0, buf[length:])
        
        return spRecordNumber
        
    def _setTextRecord(self, recordNumber, record, spRecordNumber):
        languageCodeBuf = array("B")
        languageCodeBuf.fromstring(record.language)
       
        textBuf = array("B")
        textBuf.fromstring(record.text)
        
        self._setRecordData(recordNumber, 0, languageCodeBuf)
        self._setRecordData(recordNumber, 1, textBuf)
        
        return spRecordNumber
        
    def _setSmartPosterRecord(self, recordNumber, record, recordsStart):
        spRecordNumber = recordsStart
        
        for spRecord in record.records:
            self._setNdefRecord(spRecordNumber, spRecord, 0, False) #No sub records
            spRecordNumber += 1
            
        return spRecordNumber
    
    def _setMIMERecord(self, recordNumber, record, spRecordNumber):
        mimeTypeBuf = array("B")
        mimeTypeBuf.fromstring(record.mimeType)
       
        dataBuf = array("B", record.data)
        
        self._setRecordData(recordNumber, 0, mimeTypeBuf)
        self._setRecordData(recordNumber, 1, dataBuf)
        
        return spRecordNumber

    def _encodePrefix(self, uri):
        prefix, length = self._transport.nfcEncodePrefix(uri)
        return prefix, length
    
    def _setRecordData(self, recordNumber, item, itemData):
        itemLength = len(itemData)
        itemOff = 0
        while itemOff < itemLength:
            chunkLength = min(CHUNK_SIZE, itemLength - itemOff)
            buf = array("B", itemData[itemOff:itemOff+chunkLength])
            self._transport.nfcSetRecordData(recordNumber, item, itemOff, buf)
            itemOff += chunkLength
