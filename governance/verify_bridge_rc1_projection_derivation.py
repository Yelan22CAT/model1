#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
baseline=json.loads((ROOT/"bridge_rc1_baseline.json").read_text(encoding="utf-8"))
frozen=json.loads((ROOT/"bridge_rc1_material_projection_v1.json").read_text(encoding="utf-8"))

REQUIRED_TOP={
    "rc","baseline_generation","semantic_generation","material_metadata_revision","evidence_revision",
    "semantic_anchors","git_blob_anchors","governance","lineage_policy","currentness_policy",
    "anchor_scope","evidence_blob_anchors","evidence_policy"
}

def require(obj,key):
    if key not in obj:
        raise ValueError(f"missing required field: {key}")
    return obj[key]

def derive(b):
    for k in REQUIRED_TOP:
        require(b,k)

    g=require(b,"governance")
    gov={
      "authoritative_location":require(g,"authoritative_location"),
      "experiment_branch_may_not_self_authorize_baseline_changes":require(g,"experiment_branch_may_not_self_authorize_baseline_changes"),
      "baseline_change_requires_separate_main_pull_request":require(g,"baseline_change_requires_separate_main_pull_request"),
      "protected_history_process_separation":require(g,"protected_history_process_separation"),
      "ruleset_id":require(g,"ruleset_id"),
      "ruleset_name":require(g,"ruleset_name"),
      "required_ruleset_properties":require(g,"required_ruleset_properties"),
      "ruleset_currentness_required":require(g,"ruleset_currentness_required")
    }

    return {
      "projection_version":"bridge-material-v1",
      "rc":b["rc"],
      "baseline_generation":b["baseline_generation"],
      "semantic_generation":b["semantic_generation"],
      "material_metadata_revision":b["material_metadata_revision"],
      "evidence_revision":b["evidence_revision"],
      "semantic_anchors":b["semantic_anchors"],
      "git_blob_anchors":b["git_blob_anchors"],
      "governance":gov,
      "lineage_policy":b["lineage_policy"],
      "currentness_policy":b["currentness_policy"],
      "anchor_scope":b["anchor_scope"],
      "evidence_blob_anchors":b["evidence_blob_anchors"],
      "evidence_policy":b["evidence_policy"]
    }

derived=derive(baseline)
expected=frozen["projection"]

if derived != expected:
    print(json.dumps({"match":False,"reason":"derived-projection-mismatch","derived":derived,"expected":expected},indent=2))
    sys.exit(2)

canonical=json.dumps(derived,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
actual=hashlib.sha256(canonical).hexdigest()
if actual != frozen["material_state_sha256"]:
    print(json.dumps({"match":False,"reason":"material-digest-mismatch","actual":actual,"expected":frozen["material_state_sha256"]},indent=2))
    sys.exit(2)

print(json.dumps({"match":True,"material_state_sha256":actual},indent=2))
