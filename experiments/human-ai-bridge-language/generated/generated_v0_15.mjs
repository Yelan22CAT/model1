// Generated from Bridge-0 v0.15. Do not hand-edit.
const SEMANTIC_UNICODE_VERSION = '15.0';
const tokens = ['0065+0301','1F44D+1F3FD','1F469+200D+1F4BB','1F1E8+1F1E6','0061+0308+0062','1F468+200D+1F469+200D+1F467+200D+1F466','000D+000A+0061','2764+FE0F'];
const PINNED_NFC = {'0065+0301':'00E9','0061+0308+0062':'00E4+0062'};

console.error('BRIDGE_UNICODE_RUNTIME runtime=' + process.versions.unicode
  + ' semantic=' + SEMANTIC_UNICODE_VERSION + ' mode=pinned_subset');

function normalizeToken(token) {
  return PINNED_NFC[token] || token;
}

function parseToken(token) {
  return token.split('+').map((part) => parseInt(part, 16));
}

function scalarToken(cps) {
  return cps.map((cp) => cp.toString(16).toUpperCase().padStart(4, '0')).join('+');
}

function isExtend(cp) {
  return (cp >= 0xFE00 && cp <= 0xFE0F)
    || (cp >= 0xE0100 && cp <= 0xE01EF)
    || (cp >= 0x1F3FB && cp <= 0x1F3FF);
}

function isRegionalIndicator(cp) {
  return cp >= 0x1F1E6 && cp <= 0x1F1FF;
}

function segmentSubset(cps) {
  const clusters = [];
  let i = 0;
  while (i < cps.length) {
    const cp = cps[i];
    const cluster = [cp];
    i += 1;
    if (cp === 0x000D && i < cps.length && cps[i] === 0x000A) {
      cluster.push(cps[i]);
      i += 1;
    } else if (isRegionalIndicator(cp)) {
      if (i < cps.length && isRegionalIndicator(cps[i])) {
        cluster.push(cps[i]);
        i += 1;
      }
    }
    while (i < cps.length && isExtend(cps[i])) {
      cluster.push(cps[i]);
      i += 1;
    }
    while (i + 1 < cps.length && cps[i] === 0x200D) {
      cluster.push(cps[i], cps[i + 1]);
      i += 2;
      while (i < cps.length && isExtend(cps[i])) {
        cluster.push(cps[i]);
        i += 1;
      }
    }
    clusters.push(cluster);
  }
  return clusters;
}

const profiles = {};
for (const token of tokens) {
  const normalizedToken = normalizeToken(token);
  const cps = parseToken(normalizedToken);
  const clusters = segmentSubset(cps);
  profiles[token] = {
    normalized: { $unicode_nfc: normalizedToken },
    clusters: clusters.map((item) => ({ $grapheme: scalarToken(item) })),
    count: { $exact_integer: String(clusters.length) },
  };
}
const result = {
  unicode_version: SEMANTIC_UNICODE_VERSION,
  profile: 'bridge_uax29_subset_v1',
  profiles,
};
process.stdout.write(JSON.stringify(result) + '\n');
