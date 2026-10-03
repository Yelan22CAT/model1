#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
p=Path(__file__).with_name("bridge_rc1_material_projection_v1.json")
obj=json.loads(p.read_text(encoding="utf-8"))
projection=obj["projection"]
canonical=json.dumps(projection,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
actual=hashlib.sha256(canonical).hexdigest()
expected=obj["material_state_sha256"]
print(json.dumps({"actual":actual,"expected":expected,"match":actual==expected},indent=2))
if actual!=expected:
    sys.exit(2)
