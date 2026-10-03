import hashlib, json, sys
from pathlib import Path

EXPECTED="26801a1b17d0ad9291bddd00cdc9d902bf286ab8657b193d12a7a2e274543abc"
obj=json.loads(Path("CORPUS_PROFILE_RC1.json").read_text(encoding="utf-8"))
canonical=json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
actual=hashlib.sha256(canonical).hexdigest()
print(json.dumps({"corpus_profile_canonical_sha256":actual,"expected":EXPECTED,"match":actual==EXPECTED},indent=2))
if actual!=EXPECTED:
    sys.exit(2)
