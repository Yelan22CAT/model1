import json, re, sys
from pathlib import Path

root=Path(__file__).resolve().parents[3]
workflow=(root/".github/workflows/bridge_rc1_public_repro.yml").read_text(encoding="utf-8")
manifest=json.loads(Path(__file__).with_name("ENVIRONMENT_MANIFEST.json").read_text(encoding="utf-8"))

errors=[]

for name, sha in manifest["github_actions"].items():
    needle=f"{name}@{sha}"
    if needle not in workflow:
        errors.append(f"missing action pin: {needle}")

for runtime, version in manifest["reference_requested_versions"].items():
    if version not in workflow:
        errors.append(f"missing runtime version in workflow: {runtime}={version}")

print(json.dumps({"errors":errors,"match":not errors},indent=2))
if errors:
    sys.exit(2)
