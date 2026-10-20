import json, sys
from pathlib import Path

root=Path(__file__).resolve().parent
readme=(root/"README.md").read_text(encoding="utf-8")
manifest=json.loads((root/"ENVIRONMENT_MANIFEST.json").read_text(encoding="utf-8"))
corpus=json.loads((root/"CORPUS_PROFILE_RC1.json").read_text(encoding="utf-8"))

checks={
    "output_digest": manifest["semantic_anchor"]["output_sha256"] in readme,
    "corpus_digest": manifest["semantic_anchor"]["corpus_sha256"] in readme,
    "verdict_digest": manifest["semantic_anchor"]["verdict_output_sha256"] in readme,
    "diagnostic_digest": manifest["semantic_anchor"]["diagnostic_output_sha256"] in readme,
    "decision_profile_digest": manifest["semantic_anchor"]["decision_profile_canonical_sha256"] in readme,
    "corpus_profile_digest": manifest["semantic_anchor"]["corpus_profile_canonical_sha256"] in readme,
    "seed": str(corpus["seed"]) in readme,
    "cases": str(corpus["cases"]) in readme,
    "python": manifest["reference_requested_versions"]["python"] in readme,
    "node": manifest["reference_requested_versions"]["node"] in readme,
    "ruby": manifest["reference_requested_versions"]["ruby"] in readme,
}
print(json.dumps({"checks":checks,"pass":all(checks.values())},indent=2))
if not all(checks.values()):
    sys.exit(2)
