#!/usr/bin/env python3
import base64, hashlib, json, os, re, sys, urllib.request, urllib.parse
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
GOV=ROOT/"governance"
PROFILE_PATH=GOV/"bridge_rc1_verification_execution_profile.json"
BASELINE_PATH=GOV/"bridge_rc1_baseline.json"

def fail(msg):
    print(json.dumps({"match":False,"reason":msg},indent=2)); sys.exit(2)

def git_blob_sha_bytes(data):
    h=hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode())
    h.update(data)
    return h.hexdigest()

def git_blob_sha(path):
    return git_blob_sha_bytes(path.read_bytes())

def fetch_github_file_meta(repo,ref,path,token):
    qpath=urllib.parse.quote(path,safe="/")
    qref=urllib.parse.quote(ref,safe="")
    url=f"https://api.github.com/repos/{repo}/contents/{qpath}?ref={qref}"
    headers={"Accept":"application/vnd.github+json","User-Agent":"bridge-rc1-execution-profile"}
    if token: headers["Authorization"]="Bearer "+token
    try:
        req=urllib.request.Request(url,headers=headers)
        with urllib.request.urlopen(req,timeout=30) as r:
            meta=json.load(r)
    except Exception as e:
        fail("remote evidence fetch failed: "+path+": "+type(e).__name__)
    if not isinstance(meta,dict) or meta.get("type")!="file":
        fail("remote evidence is not a regular file: "+path)
    if meta.get("path")!=path:
        fail("remote evidence path mismatch: "+path)
    if meta.get("encoding")!="base64" or not isinstance(meta.get("content"),str):
        fail("remote evidence content unavailable: "+path)
    try:
        raw=base64.b64decode("".join(meta["content"].split()),validate=True)
    except Exception:
        fail("remote evidence invalid base64: "+path)
    return meta,raw

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

token=os.environ.get("GITHUB_TOKEN","")
public_cfg=profile["public_reproduction"]
repo=public_cfg["repository_full_name"]
ref=public_cfg["workflow_ref"]
path=public_cfg["workflow_path"]

meta,raw=fetch_github_file_meta(repo,ref,path,token)
expected_workflow=baseline["git_blob_anchors"]["bridge_rc1_public_repro.yml"]
if meta.get("sha")!=expected_workflow or git_blob_sha_bytes(raw)!=expected_workflow:
    fail("public reproduction workflow blob mismatch")
public_text=raw.decode("utf-8")
require_enforced_commands(public_text,public_cfg["required_commands"],"public")

root=public_cfg["evidence_root"].rstrip("/")
for rel in public_cfg["required_evidence"]:
    if rel not in anchors: fail("public required evidence not protected: "+rel)
    if "/" in rel or rel in (".",".."):
        fail("public evidence name must be a single path component: "+rel)
    remote_path=root+"/"+rel
    emeta,eraw=fetch_github_file_meta(repo,ref,remote_path,token)
    expected=anchors[rel]
    if emeta.get("sha")!=expected:
        fail("public remote evidence metadata blob mismatch: "+rel)
    if git_blob_sha_bytes(eraw)!=expected:
        fail("public remote evidence content blob mismatch: "+rel)
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
