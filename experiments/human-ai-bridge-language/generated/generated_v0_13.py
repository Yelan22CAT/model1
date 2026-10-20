# Generated from Bridge-0 v0.13. Do not hand-edit.
import json
import math

tokens = ['nan', '+inf', '-inf', '-0', '+0', '2.5', '3.5', '-2.5', '-3.5']

def decode(token):
    if token == 'nan':
        return float('nan')
    if token == '+inf':
        return float('inf')
    if token == '-inf':
        return float('-inf')
    if token == '-0':
        return -0.0
    if token == '+0':
        return 0.0
    return float(token)

def classify(value):
    if math.isnan(value):
        return {'$binary64': 'nan'}
    if math.isinf(value):
        return {'$binary64': '+inf' if value > 0 else '-inf'}
    if value == 0.0:
        return {'$binary64': '-0' if math.copysign(1.0, value) < 0 else '+0'}
    return {'$binary64': format(value, '.17g')}

def exact_integer(value):
    return {'$exact_integer': str(value)}

values = [(token, decode(token)) for token in tokens]
result = {
    'classes': {token: classify(value) for token, value in values},
    'rounded': {
        token: exact_integer(round(value))
        for token, value in values
        if token.endswith('.5')
    },
}
print(json.dumps(result, sort_keys=True, separators=(',', ':')))
