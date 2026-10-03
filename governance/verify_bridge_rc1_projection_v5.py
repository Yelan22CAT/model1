#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SAFE=9007199254740991

class NonIntegerNumber(ValueError):
    pass

def reject_float(token):
    raise NonIntegerNumber("non-integer JSON number: "+token)

def parse_int_exact(token):
    value=int(token,10)
    if value < -SAFE or value > SAFE:
        raise NonIntegerNumber("integer outside safe-integer-v1: "+token)
    return value

def load_strict(path):
    raw=path.read_text(encoding="ascii")
    return json.loads(raw,parse_float=reject_float,parse_int=parse_int_exact)

baseline=load_strict(ROOT/"bridge_rc1_baseline.json")
frozen=load_strict(ROOT/"bridge_rc1_material_projection_v5.json")

MATERIAL_TOP={
    "rc","baseline_generation","semantic_generation","material_metadata_revision","evidence_revision",
    "semantic_anchors","git_blob_anchors","governance","lineage_policy","currentness_policy",
    "anchor_scope","evidence_blob_anchors","evidence_policy"
}
EXCLUDED_TOP={
    "name","status","previous_baseline_blob_sha","predecessor_baseline_blob_sha","created_from_pr",
    "proposed_against_main_commit","metadata_revision","previous_metadata_blob_sha","revision_policy",
    "last_anchor_update","external_repository_witness","external_repository_witness_history",
    "external_witness_policy","witness_index_revision","current_external_witness",
    "legacy_metadata_revision","material_projection"
}
MATERIAL_GOV={
    "authoritative_location",
    "experiment_branch_may_not_self-authorize_baseline_changes",
    "baseline_change_requires_separate_main_pull_request",
    "ci_pass_is_not_independent_certification",
    "protected_history_process_separation",
    "independent_principal_approval",
    "required_approving_review_count_observed",
    "third_party_certification",
    "claim_scope",
    "ruleset_id","ruleset_name","required_ruleset_properties","ruleset_currentness_required"
}
EXCLUDED_GOV={"ruleset_updated_at_observed"}

def fail(msg):
    print(json.dumps({"match":False,"reason":msg},indent=2))
    sys.exit(2)

def require(obj,key):
    if key not in obj: fail("missing required field: "+key)
    return obj[key]

def validate_types(v,path="$"):
    if isinstance(v,float):
        fail("float material value at "+path)
    if isinstance(v,int) and not isinstance(v,bool):
        if v < -SAFE or v > SAFE:
            fail("unsafe integer at "+path)
    if isinstance(v,str):
        try: v.encode("ascii")
        except UnicodeEncodeError: fail("non-ASCII material string at "+path)
    elif isinstance(v,list):
        for i,x in enumerate(v): validate_types(x,f"{path}[{i}]")
    elif isinstance(v,dict):
        for k,val in v.items():
            try: k.encode("ascii")
            except UnicodeEncodeError: fail("non-ASCII material key at "+path)
            validate_types(val,f"{path}.{k}")

unknown_top=set(baseline)-MATERIAL_TOP-EXCLUDED_TOP
if unknown_top: fail("unknown top-level fields: "+",".join(sorted(unknown_top)))
g=require(baseline,"governance")
unknown_gov=set(g)-MATERIAL_GOV-EXCLUDED_GOV
if unknown_gov: fail("unknown governance fields: "+",".join(sorted(unknown_gov)))
for k in MATERIAL_GOV: require(g,k)

derived={
  "projection_version":"bridge-material-v5",
  "text_profile":"ascii-v1",
  "number_profile":"safe-integer-v1",
  "rc":require(baseline,"rc"),
  "baseline_generation":require(baseline,"baseline_generation"),
  "semantic_generation":require(baseline,"semantic_generation"),
  "material_metadata_revision":require(baseline,"material_metadata_revision"),
  "evidence_revision":require(baseline,"evidence_revision"),
  "semantic_anchors":require(baseline,"semantic_anchors"),
  "git_blob_anchors":require(baseline,"git_blob_anchors"),
  "governance":{k:g[k] for k in sorted(MATERIAL_GOV)},
  "lineage_policy":require(baseline,"lineage_policy"),
  "currentness_policy":require(baseline,"currentness_policy"),
  "anchor_scope":require(baseline,"anchor_scope"),
  "evidence_blob_anchors":require(baseline,"evidence_blob_anchors"),
  "evidence_policy":require(baseline,"evidence_policy")
}
validate_types(derived)
if derived != frozen["projection"]: fail("derived-projection-mismatch")

canonical=json.dumps(derived,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
actual=hashlib.sha256(canonical).hexdigest()
if actual != frozen["material_state_sha256"]: fail("material-digest-mismatch")
print(json.dumps({"match":True,"projection_version":"bridge-material-v5","text_profile":"ascii-v1","number_profile":"safe-integer-v1","material_state_sha256":actual},indent=2))
