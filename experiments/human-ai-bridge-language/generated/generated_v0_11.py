# Generated from Bridge-0 v0.11. Do not hand-edit.
import json

values = [2, 3, 5, 7, 11, 13]
result = {
    'count': len(values),
    'max': max(values),
    'min': min(values),
    'sum': sum(values),
}
print(json.dumps(result, sort_keys=True, separators=(',', ':')))
