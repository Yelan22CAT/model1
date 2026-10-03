#!/usr/bin/env python3
import json, os, sys, urllib.request
from pathlib import Path

event=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
repo=event["repository"]["full_name"]
head_sha=event["pull_request"]["head"]["sha"]
token=os.environ["GITHUB_TOKEN"]

baseline=json.loads(Path("governance/bridge_rc1_baseline.json").read_text(encoding="utf-8"))
mapping={
  "SPEC_v1.0-rc1.md":"experiments/human-ai-bridge-language/SPEC_v1.0-rc1.md",
  "COMPATIBILITY_v1.0-rc1.md":"experiments/human-ai-bridge-language/COMPATIBILITY_v1.0-rc1.md",
  "INVARIANTS_RC1.json":"experiments/human-ai-bridge-language/INVARIANTS_RC1.json",
  "DECISION_PROFILE_RC1.json":"experiments/human-ai-bridge-language/public_repro_rc1/DECISION_PROFILE_RC1.json",
  "CORPUS_PROFILE_RC1.json":"experiments/human-ai-bridge-language/public_repro_rc1/CORPUS_PROFILE_RC1.json",
  "ENVIRONMENT_MANIFEST.json":"experiments/human-ai-bridge-language/public_repro_rc1/ENVIRONMENT_MANIFEST.json",
  "bridge_rc1_public_repro.yml":".github/workflows/bridge_rc1_public_repro.yml"
}

def github_json(url):
    req=urllib.request.Request(
        url,
        headers={
            "Authorization":f"Bearer {token}",
            "Accept":"application/vnd.github+json",
            "X-GitHub-Api-Version":"2022-11-28",
            "User-Agent":"bridge-rc1-baseline-check"
        }
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)

errors=[]
rows=[]
for name,path in mapping.items():
    expected=baseline["git_blob_anchors"][name]
    url=f"https://api.github.com/repos/{repo}/contents/{path}?ref={head_sha}"
    try:
        meta=github_json(url)
        actual=meta["sha"]
        match=(actual==expected)
    except Exception as e:
        actual=None
        match=False
        errors.append(f"{name}: fetch failed: {e}")
    rows.append({"name":name,"path":path,"expected":expected,"actual":actual,"match":match})
    if not match and actual is not None:
        errors.append(f"{name}: baseline drift")

print(json.dumps({
    "protected_baseline_commit": os.environ.get("GITHUB_SHA"),
    "pr_head_sha": head_sha,
    "checks": rows,
    "match": not errors,
    "errors": errors
},indent=2))

if errors:
    sys.exit(2)
