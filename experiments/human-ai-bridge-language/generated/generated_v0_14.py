# Generated from Bridge-0 v0.14. Do not hand-edit.
import json
import unicodedata

tokens = ['00E9', '0065+0301', '00C5', '0041+030A', '212B', 'AC00', '1100+1161', '0065+0323+0301', '0065+0301+0323', '1F600', '1F469+200D+1F4BB']

def decode(token):
    return ''.join(chr(int(part, 16)) for part in token.split('+'))

def scalar_token(text):
    return '+'.join(f'{ord(ch):04X}' for ch in text)

normalized = {}
for token in tokens:
    text = decode(token)
    nfc = unicodedata.normalize('NFC', text)
    normalized[token] = {'$unicode_nfc': scalar_token(nfc)}

result = {'normalized': normalized}
print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
