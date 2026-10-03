// Generated from Bridge-0 v0.14. Do not hand-edit.
const tokens = ['00E9','0065+0301','00C5','0041+030A','212B','AC00','1100+1161','0065+0323+0301','0065+0301+0323','1F600','1F469+200D+1F4BB'];

function decode(token) {
  return String.fromCodePoint(...token.split('+').map((part) => parseInt(part, 16)));
}

function scalarToken(text) {
  return Array.from(text, (ch) => ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')).join('+');
}

const normalized = {};
for (const token of tokens) {
  const text = decode(token);
  const nfc = text.normalize('NFC');
  normalized[token] = { $unicode_nfc: scalarToken(nfc) };
}
const result = { normalized };
process.stdout.write(JSON.stringify(result) + '\n');
