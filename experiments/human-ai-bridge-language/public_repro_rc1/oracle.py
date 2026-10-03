import json
import sys

profile = json.load(open(sys.argv[1], encoding="utf-8"))
rows = json.load(open(sys.argv[2], encoding="utf-8"))

for item in rows:
    state = item["state"]
    result = True
    reason = "ok"
    for gate in profile["ordered_gates"]:
        current = state[gate["field"]]
        if gate["op"] == "eq":
            passed = current == gate["value"]
        elif gate["op"] == "gte_field":
            passed = current >= state[gate["value"]]
        else:
            passed = False
        if not passed:
            result = False
            reason = gate["reason"]
            break
    print(str(item["id"]) + "|" + ("1" if result else "0") + "|" + reason)
