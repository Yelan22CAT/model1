#!/usr/bin/env python3
import base64, hashlib, json, os, sys, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
GOV=ROOT/"governance"
PROFILE_PATH=GOV/"bridge_rc1_verification_execution_profile.json"
BASELINE_PATH=GOV/"bridge_rc1_baseline.json"
GOV_WF=ROOT/".github/workflows/bridge_rc1_governance_verify.yml"

def fail(msg):
    print(json.dumps({"match":False,"reason":msg},indent=2)); sys.exit(2)

def git_blob_sha(path):
    data=path.read_bytes()
    h=hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode())
    h.update(data)
    return h.hexdigest()

profile=json.loads(PROFILE_PATH.read_text())
baseline=json.loads(BASELINE_PATH.read_text())
anchors=baseline["evidence_blob_anchors"]

# Local protected-main governance evidence identity.
for rel in profile["governance_material"]["required_evidence"]:
    path=ROOT/rel
    if not path.exists(): fail("missing governance evidence: "+rel)
    if anchors.get(rel)!=git_blob_sha(path): fail("governance evidence blob mismatch: "+rel)

gov_wf_rel=profile["governance_material"]["workflow_path"]
if anchors.get(gov_wf_rel)!=git_blob_sha(ROOT/gov_wf_rel):
    fail("governance workflow blob mismatch")

gov_text=(ROOT/gov_wf_rel).read_text()
for cmd in profile["governance_material"]["required_commands"]:
    if cmd not in gov_text: fail("governance command not executed: "+cmd)

# Public reproduction workflow is fetched by exact branch ref and must match
# the protected baseline blob identity before command coverage is trusted.
repo=os.environ.get("GITHUB_REPOSITORY","Yelan22CAT/model1")
token=os.environ.get("GITHUB_TOKEN","")
ref=profile["public_reproduction"]["workflow_ref"]
path=profile["public_reproduction"]["workflow_path"]
url=f"https://api.github.com/repos/{repo}/contents/{path}?ref={ref}"
headers={"Accept":"application/vnd.github+json","User-Agent":"bridge-rc1-execution-profile"}
if token: headers["Authorization"]="Bearer "+token
req=urllib.request.Request(url,headers=headers)
with urllib.request.urlopen(req) as r:
    meta=json.load(r)
if meta.get("sha")!=baseline["git_blob_anchors"]["bridge_rc1_public_repro.yml"]:
    fail("public reproduction workflow blob mismatch")
public_text=base64.b64decode(meta["content"]).decode()
for cmd in profile["public_reproduction"]["required_commands"]:
    if cmd not in public_text: fail("public command not executed: "+cmd)

# Every current required evidence artifact must be protected.
for rel in profile["public_reproduction"]["required_evidence"]:
    if rel not in anchors: fail("public required evidence not protected: "+rel)
for rel in profile["governance_material"]["required_evidence"]:
    if rel not in anchors: fail("governance required evidence not protected: "+rel)

current=set(profile["public_reproduction"]["required_evidence"]) | set(profile["governance_material"]["required_evidence"])
historical=set(profile["historical_evidence"])
protected=set(anchors)
unclassified=protected-current-historical
if unclassified: fail("protected evidence unclassified: "+",".join(sorted(unclassified)))
if current & historical: fail("evidence classified both current and historical")

print(json.dumps({
  "match":True,
  "profile_id":profile["profile_id"],
  "current_required_count":len(current),
  "historical_count":len(historical),
  "unclassified_count":0
},indent=2))
