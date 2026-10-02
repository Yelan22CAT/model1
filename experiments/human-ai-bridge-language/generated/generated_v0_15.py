# Generated from Bridge-0 v0.15. Do not hand-edit.
import json
import sys
import unicodedata

SEMANTIC_UNICODE_VERSION = '15.0'
tokens = ['0065+0301', '1F44D+1F3FD', '1F469+200D+1F4BB', '1F1E8+1F1E6', '0061+0308+0062', '1F468+200D+1F469+200D+1F467+200D+1F466', '000D+000A+0061', '2764+FE0F']
PINNED_NFC = {'0065+0301': '00E9', '0061+0308+0062': '00E4+0062'}

print(
    'BRIDGE_UNICODE_RUNTIME runtime=' + unicodedata.unidata_version
    + ' semantic=' + SEMANTIC_UNICODE_VERSION
    + ' mode=pinned_subset',
    file=sys.stderr,
)

def normalize_token(token):
    return PINNED_NFC.get(token, token)

def parse_token(token):
    return [int(part, 16) for part in token.split('+')]

def scalar_token(cps):
    return '+'.join(f'{cp:04X}' for cp in cps)

def is_extend(cp):
    return (
        0xFE00 <= cp <= 0xFE0F
        or 0xE0100 <= cp <= 0xE01EF
        or 0x1F3FB <= cp <= 0x1F3FF
    )

def is_regional_indicator(cp):
    return 0x1F1E6 <= cp <= 0x1F1FF

def segment_subset(cps):
    clusters = []
    i = 0
    while i < len(cps):
        cp = cps[i]
        cluster = [cp]
        i += 1
        if cp == 0x000D and i < len(cps) and cps[i] == 0x000A:
            cluster.append(cps[i])
            i += 1
        elif is_regional_indicator(cp):
            if i < len(cps) and is_regional_indicator(cps[i]):
                cluster.append(cps[i])
                i += 1
        while i < len(cps) and is_extend(cps[i]):
            cluster.append(cps[i])
            i += 1
        while i + 1 < len(cps) and cps[i] == 0x200D:
            cluster.extend([cps[i], cps[i + 1]])
            i += 2
            while i < len(cps) and is_extend(cps[i]):
                cluster.append(cps[i])
                i += 1
        clusters.append(cluster)
    return clusters

profiles = {}
for token in tokens:
    normalized_token = normalize_token(token)
    cps = parse_token(normalized_token)
    clusters = segment_subset(cps)
    profiles[token] = {
        'normalized': {'$unicode_nfc': normalized_token},
        'clusters': [{'$grapheme': scalar_token(item)} for item in clusters],
        'count': {'$exact_integer': str(len(clusters))},
    }

result = {
    'unicode_version': SEMANTIC_UNICODE_VERSION,
    'profile': 'bridge_uax29_subset_v1',
    'profiles': profiles,
}
print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
