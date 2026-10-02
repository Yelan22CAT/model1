# Generated from Bridge-0 v0.15. Do not hand-edit.
import json
import unicodedata

PINNED_UNICODE_VERSION = '15.0'
tokens = ['0065+0301', '1F44D+1F3FD', '1F469+200D+1F4BB', '1F1E8+1F1E6', '0061+0308+0062', '1F468+200D+1F469+200D+1F467+200D+1F466', '000D+000A+0061', '2764+FE0F']

def version_matches(runtime, pinned):
    return runtime == pinned or runtime.startswith(pinned + '.')

if not version_matches(unicodedata.unidata_version, PINNED_UNICODE_VERSION):
    raise RuntimeError(
        'Unicode data version mismatch: ' + unicodedata.unidata_version
        + ' != ' + PINNED_UNICODE_VERSION
    )

def decode(token):
    return ''.join(chr(int(part, 16)) for part in token.split('+'))

def scalar_token(text):
    return '+'.join(f'{ord(ch):04X}' for ch in text)

def is_extend(cp):
    return (
        unicodedata.category(chr(cp)).startswith('M')
        or 0xFE00 <= cp <= 0xFE0F
        or 0xE0100 <= cp <= 0xE01EF
        or 0x1F3FB <= cp <= 0x1F3FF
    )

def is_regional_indicator(cp):
    return 0x1F1E6 <= cp <= 0x1F1FF

def segment_subset(text):
    cps = [ord(ch) for ch in text]
    clusters = []
    i = 0
    ri_run = 0
    while i < len(cps):
        cp = cps[i]
        cluster = [cp]
        i += 1
        if cp == 0x000D and i < len(cps) and cps[i] == 0x000A:
            cluster.append(cps[i])
            i += 1
            ri_run = 0
        elif is_regional_indicator(cp):
            ri_run += 1
            if i < len(cps) and is_regional_indicator(cps[i]) and ri_run % 2 == 1:
                cluster.append(cps[i])
                i += 1
                ri_run += 1
        else:
            ri_run = 0
        while i < len(cps) and is_extend(cps[i]):
            cluster.append(cps[i])
            i += 1
        while i + 1 < len(cps) and cps[i] == 0x200D:
            cluster.append(cps[i])
            cluster.append(cps[i + 1])
            i += 2
            while i < len(cps) and is_extend(cps[i]):
                cluster.append(cps[i])
                i += 1
        clusters.append(''.join(chr(value) for value in cluster))
    return clusters

profiles = {}
for token in tokens:
    nfc = unicodedata.normalize('NFC', decode(token))
    clusters = segment_subset(nfc)
    profiles[token] = {
        'normalized': {'$unicode_nfc': scalar_token(nfc)},
        'clusters': [{'$grapheme': scalar_token(item)} for item in clusters],
        'count': {'$exact_integer': str(len(clusters))},
    }

result = {
    'unicode_version': PINNED_UNICODE_VERSION,
    'profile': 'bridge_uax29_subset_v1',
    'profiles': profiles,
}
print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
