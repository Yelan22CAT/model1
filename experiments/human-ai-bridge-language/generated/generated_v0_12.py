# Generated from Bridge-0 v0.12. Do not hand-edit.
import json

values = [9007199254740991, 9007199254740993, -9007199254740995, 18446744073709551617]
def exact(value):
    return {'$exact_integer': str(value)}

result = {
    'count': exact(len(values)),
    'max': exact(max(values)),
    'min': exact(min(values)),
    'sum': exact(sum(values)),
}
print(json.dumps(result, sort_keys=True, separators=(',', ':')))
