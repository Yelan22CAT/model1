#!/usr/bin/env python3
import base64, hashlib, json, os, re, sys, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
GOV=ROOT/"governance"
PROFILE_PATH=GOV/"bridge_rc1_verification_execution_profile.json"
BASELINE_PATH=GOV/"bridge_rc1_baseline.json"

def fail(msg):
    print(json.dumps({"match":False,"reason":msg},indent=2)); sys.exit(2)

def git_blob_sha(path):
    data=path.read_bytes()
    h=hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode())
    h.update(data)
    return h.hexdigest()

def parse_named_steps(text):
    lines=text.splitlines()
    steps=[]
    cur=None
    i=0
    while i < len(lines):
        line=lines[i]
        m=re.match(r'^\s*-\s+name:\s*(.+)$',line)
        if m:
            if cur: steps.append(cur)
            cur={"name":m.group(1).strip(),"run":[],"continue_on_error":False,"if":None}
            i+=1; continue
        if cur is None:
            i+=1; continue
        m=re.match(r'^\s*continue-on-error:\s*(true|false)\s*$',line)
        if m:
            cur["continue_on_error"]=(m.group(1)=="true"); i+=1; continue
        m=re.match(r'^\s*if:\s*(.+?)\s*$',line)
        if m:
            cur["if"]=m.group(1).strip(); i+=1; continue
        m=re.match(r'^\s*run:\s*(.*?)\s*$',line)
        if m:
            rhs=m.group(1)
            if rhs in ("|",">"):
                base=len(line)-len(line.lstrip())
                i+=1
                while i < len(lines):
                    nxt=lines[i]
                    if not nxt.strip():
                        i+=1; continue
                    indent=len(nxt)-len(nxt.lstrip())
                    if indent <= base: break
                    stripped=nxt.strip()
                    if not stripped.startswith("#"):
                        cur["run"].append(stripped)
                    i+=1
                continue
            elif rhs:
                cur["run"].append(rhs.strip())
        i+=1
    if cur: steps.append(cur)
    return steps

def require_enforced_commands(text,required,label):
    steps=parse_named_steps(text)
    for cmd in required:
        matches=[]
        for step in steps:
            if cmd in step["run"]:
                matches.append(step)
        if not matches:
            fail(label+" command not executed: "+cmd)
        enforced=[
            s for s in matches
            if not s["continue_on_error"] and s["if"] is None
        ]
        if not enforced:
            fail(label+" command not enforced: "+cmd)

profile=json.loads(PROFILE_PATH.read_text())
baseline=json.loads(BASELINE_PATH.read_text())
anchors=baseline["evidence_blob_anchors"]

for rel in profile["governance_material"]["required_evidence"]:
    path=ROOT/rel
    if not path.exists(): fail("missing governance evidence: "+rel)
    if anchors.get(rel)!=git_blob_sha(path): fail("governance evidence blob mismatch: "+rel)

gov_wf_rel=profile["governance_material"]["workflow_path"]
if anchors.get(gov_wf_rel)!=git_blob_sha(ROOT/gov_wf_rel):
    fail("governance workflow blob mismatch")
gov_text=(ROOT/gov_wf_rel).read_text()
require_enforced_commands(gov_text,profile["governance_material"]["required_commands"],"governance")

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
require_enforced_commands(public_text,profile["public_reproduction"]["required_commands"],"public")

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
  "execution_match_profile":"constrained-run-step-v2",
  "current_required_count":len(current),
  "historical_count":len(historical),
  "unclassified_count":0
},indent=2))
