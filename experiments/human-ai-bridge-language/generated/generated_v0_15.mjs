// Generated from Bridge-0 v0.15. Do not hand-edit.
const PINNED_UNICODE_VERSION = '15.0';
const tokens = ['0065+0301','1F44D+1F3FD','1F469+200D+1F4BB','1F1E8+1F1E6','0061+0308+0062','1F468+200D+1F469+200D+1F467+200D+1F466','000D+000A+0061','2764+FE0F'];

function versionMatches(runtime, pinned) {
  return runtime === pinned || runtime.startsWith(pinned + '.');
}

if (!versionMatches(process.versions.unicode, PINNED_UNICODE_VERSION)) {
  throw new Error('Unicode data version mismatch: ' + process.versions.unicode + ' != ' + PINNED_UNICODE_VERSION);
}

function decode(token) {
  return String.fromCodePoint(...token.split('+').map((part) => parseInt(part, 16)));
}

function scalarToken(text) {
  return Array.from(text, (ch) => ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')).join('+');
}

const segmenter = new Intl.Segmenter('en', { granularity: 'grapheme' });
const profiles = {};
for (const token of tokens) {
  const nfc = decode(token).normalize('NFC');
  const clusters = Array.from(segmenter.segment(nfc), (entry) => entry.segment);
  profiles[token] = {
    normalized: { $unicode_nfc: scalarToken(nfc) },
    clusters: clusters.map((item) => ({ $grapheme: scalarToken(item) })),
    count: { $exact_integer: String(clusters.length) },
  };
}
const result = {
  unicode_version: PINNED_UNICODE_VERSION,
  profile: 'bridge_uax29_subset_v1',
  profiles,
};
process.stdout.write(JSON.stringify(result) + '\n');
