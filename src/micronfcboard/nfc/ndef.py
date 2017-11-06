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

class Record(object):
    def __init__(self, recordType):
        self._type = recordType
        pass
    
    @property
    def type(self):
        return self._type
    
    def __str__(self):
        return "%s Record" % (self._type,)
        
class URIRecord(Record):
    def __init__(self, uri = None):
        super(URIRecord, self).__init__("URI")
        self._uri = uri
        
    @property
    def uri(self):
        return self._uri
    
    def __str__(self):
        return Record.__str__(self) + ": URI = %s" % (self._uri,)
    
class TextRecord(Record):
    def __init__(self, text = None, language = None, encoding="utf-8"):
        super(TextRecord, self).__init__("Text")
        self._text = text
        self._language = language
        self._encoding = encoding
        
    @property
    def text(self):
        return self._text
    
    @property
    def language(self):
        return self._language
    
    @property
    def encoding(self):
        return self._encoding
    
    def __str__(self):
        return Record.__str__(self) + ": Language = %s, Text = %s, Encoding = %s" % (self._language, self.text, self.encoding)
    
class SmartPosterRecord(Record):
    def __init__(self, records = []):
        super(SmartPosterRecord, self).__init__("Smart Poster")
        if records == None:
            records = []
        self._records = records
        
    @property
    def records(self):
        return self._records
    
    def __str__(self):
        text = Record.__str__(self)
        for r in self._records:
            text += "\r\n\t" + r.__str__()
        return text
    
class MIMERecord(Record):
    def __init__(self, mimeType = None, data = None):
        super(MIMERecord, self).__init__("MIME")
        self._mimeType = mimeType
        self._data = data
        
    @property
    def mimeType(self):
        return self._mimeType
    
    @property
    def data(self):
        return self._data
    
    def __str__(self):
        return Record.__str__(self) + ": Type = %s, Data Length = %d" % (self._mimeType, len(self._data))
