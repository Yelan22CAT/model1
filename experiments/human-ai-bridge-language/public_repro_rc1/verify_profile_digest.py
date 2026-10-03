import hashlib, json, sys
from pathlib import Path

EXPECTED="9631290649bcd4af41cd565074051f0b145771d9ec77b8397091f14861a59a1a"
obj=json.loads(Path("DECISION_PROFILE_RC1.json").read_text(encoding="utf-8"))
canonical=json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
actual=hashlib.sha256(canonical).hexdigest()
print(json.dumps({"decision_profile_canonical_sha256":actual,"expected":EXPECTED,"match":actual==EXPECTED},indent=2))
if actual!=EXPECTED:
    sys.exit(2)
