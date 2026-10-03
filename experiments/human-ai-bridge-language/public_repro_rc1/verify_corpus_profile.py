import hashlib, json, sys
from pathlib import Path

EXPECTED="4fb956e92acc20d6f54fee1a6b4805d23402a36e12856a6684d122ec2f275f38"
obj=json.loads(Path("CORPUS_PROFILE_RC1.json").read_text(encoding="utf-8"))
canonical=json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
actual=hashlib.sha256(canonical).hexdigest()
print(json.dumps({"corpus_profile_canonical_sha256":actual,"expected":EXPECTED,"match":actual==EXPECTED},indent=2))
if actual!=EXPECTED:
    sys.exit(2)
