#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SAFE=9007199254740991
class MaterialParseError(ValueError): pass

def reject_float(token): raise MaterialParseError("non-integer JSON number: "+token)
def parse_int_exact(token):
    value=int(token,10)
    if value < -SAFE or value > SAFE: raise MaterialParseError("integer outside safe-integer-v1: "+token)
    return value
def reject_duplicate_pairs(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise MaterialParseError("duplicate JSON object key: "+k)
        out[k]=v
    return out
def load_strict(path):
    raw=path.read_text(encoding="ascii")
    return json.loads(raw,parse_float=reject_float,parse_int=parse_int_exact,object_pairs_hook=reject_duplicate_pairs)

baseline=load_strict(ROOT/"bridge_rc1_baseline.json")
frozen=load_strict(ROOT/"bridge_rc1_material_projection_v13.json")

MATERIAL_TOP={"rc","baseline_generation","semantic_generation","material_metadata_revision","evidence_revision","verification_execution_profile_blob_sha","semantic_anchors","git_blob_anchors","governance","lineage_policy","currentness_policy","anchor_scope","evidence_blob_anchors","evidence_policy"}
EXCLUDED_TOP={"name","status","previous_baseline_blob_sha","predecessor_baseline_blob_sha","created_from_pr","proposed_against_main_commit","metadata_revision","previous_metadata_blob_sha","revision_policy","last_anchor_update","external_repository_witness","external_repository_witness_history","external_witness_policy","witness_index_revision","current_external_witness","legacy_metadata_revision","material_projection","current_witness_selector","witness_lineage_policy"}
MATERIAL_GOV={"authoritative_location","experiment_branch_may_not_self-authorize_baseline_changes","baseline_change_requires_separate_main_pull_request","ci_pass_is_not_independent_certification","protected_history_process_separation","independent_principal_approval","required_approving_review_count_observed","third_party_certification","claim_scope","ruleset_id","ruleset_name","required_ruleset_properties","ruleset_currentness_required"}
EXCLUDED_GOV={"ruleset_updated_at_observed"}

def fail(msg):
    print(json.dumps({"match":False,"reason":msg},indent=2)); sys.exit(2)
def require(obj,key):
    if key not in obj: fail("missing required field: "+key)
    return obj[key]
def is_int(v): return type(v) is int
def is_bool(v): return type(v) is bool
def is_str(v): return type(v) is str
def dict_str_str(v): return type(v) is dict and all(is_str(k) and is_str(x) for k,x in v.items())
def dict_str_bool(v): return type(v) is dict and all(is_str(k) and is_bool(x) for k,x in v.items())
def list_str(v): return type(v) is list and all(is_str(x) for x in v)
def printable(s): return is_str(s) and all(0x20 <= ord(ch) <= 0x7e for ch in s)

def schema_check(d):
    if not is_str(d["rc"]): fail("type:rc")
    for k in ("baseline_generation","semantic_generation","material_metadata_revision","evidence_revision"):
        if not is_int(d[k]): fail("type:"+k)
    if not is_str(d["verification_execution_profile_blob_sha"]): fail("type:verification_execution_profile_blob_sha")
    if not dict_str_str(d["semantic_anchors"]): fail("type:semantic_anchors")
    if not dict_str_str(d["git_blob_anchors"]): fail("type:git_blob_anchors")
    if not dict_str_str(d["evidence_blob_anchors"]): fail("type:evidence_blob_anchors")
    g=d["governance"]
    for k in ("authoritative_location","claim_scope","ruleset_name"):
        if not is_str(g[k]): fail("type:governance."+k)
    for k in ("experiment_branch_may_not_self-authorize_baseline_changes","baseline_change_requires_separate_main_pull_request","ci_pass_is_not_independent_certification","protected_history_process_separation","independent_principal_approval","third_party_certification","ruleset_currentness_required"):
        if not is_bool(g[k]): fail("type:governance."+k)
    for k in ("required_approving_review_count_observed","ruleset_id"):
        if not is_int(g[k]): fail("type:governance."+k)
    rp=g["required_ruleset_properties"]
    if not is_str(rp["enforcement"]): fail("type:ruleset.enforcement")
    for k in ("deletion_rule_required","non_fast_forward_rule_required","pull_request_rule_required","no_bypass_actors_observed"):
        if not is_bool(rp[k]): fail("type:ruleset."+k)
    if not is_int(rp["required_approving_review_count_observed"]): fail("type:ruleset.approval_count")
    for section in ("lineage_policy","currentness_policy","evidence_policy"):
        if not dict_str_bool(d[section]): fail("type:"+section)
    a=d["anchor_scope"]
    for k in ("protected_exact_blob_anchors","implementation_files_not_exactly_frozen"):
        if not list_str(a[k]): fail("type:anchor_scope."+k)
    for k in ("implementation_refactor_allowed_only_if_anchored_semantic_digests_remain_unchanged","implementation_change_that_changes_corpus_or_output_digest_requires_revalidation","readme_is_informative_not_normative","unanchored_implementation_identity_is_not_part_of_the_protected_baseline_claim","evidence_implementation_exactly_anchored","implementation_refactor_allowed_only_after_separate_main_reanchor"):
        if not is_bool(a[k]): fail("type:anchor_scope."+k)

def validate_repertoire(v,path="$"):
    if v is None: fail("null not allowed at "+path)
    if isinstance(v,str):
        if not printable(v): fail("non-printable-ASCII at "+path)
    elif isinstance(v,list):
        for i,x in enumerate(v): validate_repertoire(x,f"{path}[{i}]")
    elif isinstance(v,dict):
        for k,val in v.items():
            if not printable(k): fail("non-printable-ASCII key at "+path)
            validate_repertoire(val,f"{path}.{k}")
    elif isinstance(v,int) and not isinstance(v,bool):
        if v < -SAFE or v > SAFE: fail("unsafe integer at "+path)
    elif isinstance(v,bool): pass
    else: fail("unsupported type at "+path)

unknown_top=set(baseline)-MATERIAL_TOP-EXCLUDED_TOP
if unknown_top: fail("unknown top-level fields: "+",".join(sorted(unknown_top)))
g=require(baseline,"governance")
unknown_gov=set(g)-MATERIAL_GOV-EXCLUDED_GOV
if unknown_gov: fail("unknown governance fields: "+",".join(sorted(unknown_gov)))
for k in MATERIAL_GOV: require(g,k)

derived={
  "projection_version":"bridge-material-v13",
  "text_profile":"printable-ascii-v1",
  "number_profile":"safe-integer-v1",
  "parser_profile":"duplicate-key-reject-v1",
  "schema_profile":"typed-governance-v1",
  "rc":require(baseline,"rc"),
  "baseline_generation":require(baseline,"baseline_generation"),
  "semantic_generation":require(baseline,"semantic_generation"),
  "material_metadata_revision":require(baseline,"material_metadata_revision"),
  "evidence_revision":require(baseline,"evidence_revision"),
  "verification_execution_profile_blob_sha":require(baseline,"verification_execution_profile_blob_sha"),
  "semantic_anchors":require(baseline,"semantic_anchors"),
  "git_blob_anchors":require(baseline,"git_blob_anchors"),
  "governance":{k:g[k] for k in sorted(MATERIAL_GOV)},
  "lineage_policy":require(baseline,"lineage_policy"),
  "currentness_policy":require(baseline,"currentness_policy"),
  "anchor_scope":require(baseline,"anchor_scope"),
  "evidence_blob_anchors":require(baseline,"evidence_blob_anchors"),
  "evidence_policy":require(baseline,"evidence_policy")
}
schema_check(derived)
validate_repertoire(derived)
if derived != frozen["projection"]: fail("derived-projection-mismatch")
canonical=json.dumps(derived,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode("ascii")
actual=hashlib.sha256(canonical).hexdigest()
if actual != frozen["material_state_sha256"]: fail("material-digest-mismatch")
print(json.dumps({"match":True,"projection_version":"bridge-material-v13","schema_profile":"typed-governance-v1","material_state_sha256":actual},indent=2))
