#!/usr/bin/env python3
"""Experimental Bridge-0 v0.20 CVE triage sidecar; no execution authority.

Provenance and exposure are *separate*: text declaring verification cannot
create trust. Trusted context MUST be supplied independently by a host; this
prototype cannot establish the host's authenticity. Never grants deployment.
"""
from __future__ import annotations
import hashlib
import json
import re
from typing import Any

class SyntaxErrorV020(ValueError):
    pass

PATTERN = re.compile(r'^(⊙|◆|○|!) \[([A-Za-z][A-Za-z0-9_-]{0,30})\] ([a-z_]+) (.+)$')
KEY = re.compile(r'^[a-z][a-z0-9_]*$')
VALUE = re.compile(r'^[A-Za-z0-9_.,:/-]{1,128}$')
CVE = re.compile(r'^CVE-[0-9]{4}-[0-9]{4,}$')
SCHEMA = [
    ('⊙', 'security_triage', {'profile'}, {'profile':'v0_20'}),
    ('◆', 'advisory', {'cve','source_ref','source_state'}, None),
    ('○', 'asset', {'asset_id','component','version','cve','affected','reachable','trust'}, None),
    ('!', 'gate', {'action','requires'}, {'action':'release','requires':'human_final'}),
]
TRI = {'yes','no','unknown'}
TRUST = {'current','revoked','unknown'}


def parse(source: str) -> dict[str, Any]:
    """Strict profile grammar, unlike earlier executable profiles.

    A document is precisely four declarations; arbitrary or duplicate fields,
    malformed IDs, and unsupported syntax fail without LLM interpretation.
    """
    lines = [x.strip() for x in source.splitlines() if x.strip() and not x.lstrip().startswith('#')]
    if len(lines) != len(SCHEMA):
        raise SyntaxErrorV020('exactly four declarations required')
    statements=[]
    seen=set()
    for idx,(line,(marker,kind,allowed,constraints)) in enumerate(zip(lines,SCHEMA),1):
        match=PATTERN.fullmatch(line)
        if not match:
            raise SyntaxErrorV020(f'line {idx}: invalid syntax')
        symbol, sid, word, raw=match.groups()
        if sid in seen or symbol!=marker or word!=kind:
            raise SyntaxErrorV020(f'line {idx}: invalid marker/kind or duplicate ID')
        seen.add(sid)
        data={}
        for token in raw.split():
            if token.count('=')!=1:
                raise SyntaxErrorV020(f'line {idx}: invalid key=value')
            key,value=token.split('=',1)
            if not KEY.fullmatch(key) or not VALUE.fullmatch(value) or key in data:
                raise SyntaxErrorV020(f'line {idx}: invalid/duplicate field')
            data[key]=value
        if set(data)!=allowed:
            raise SyntaxErrorV020(f'line {idx}: exact fields required {sorted(allowed)}')
        if constraints and any(data.get(k)!=v for k,v in constraints.items()):
            raise SyntaxErrorV020(f'line {idx}: unsupported profile/authority')
        statements.append({'id':sid,'kind':kind,**data})
    _,adv,asset,_=statements
    if not CVE.fullmatch(adv['cve']) or adv['cve']!=asset['cve']:
        raise SyntaxErrorV020('CVE id mismatch or invalid')
    if adv['source_state'] not in {'claimed','verified','unknown'}:
        raise SyntaxErrorV020('invalid source state')
    if asset['affected'] not in TRI or asset['reachable'] not in TRI or asset['trust'] not in TRUST:
        raise SyntaxErrorV020('invalid typed state')
    if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_.-]{1,60}',asset['asset_id']):
        raise SyntaxErrorV020('invalid asset id')
    return {'language':'Bridge-0','version':'0.20-candidate','mode':'advisory_only','statements':statements}


def evaluate(doc:dict[str,Any],trusted_context:dict[str,Any]|None) -> dict[str,Any]:
    """Read-only triage. Never resolves trust from self-declared `verified`.

    Trusted context is externally provisioned; this sidecar *does not* prove it
    was signed, timely, or unpoisoned. All execution_allowed are always False.
    """
    if doc.get('version')!='0.20-candidate' or doc.get('mode')!='advisory_only':
        raise SyntaxErrorV020('unsupported document version/mode')
    s=doc.get('statements')
    if not isinstance(s,list) or len(s)!=4 or any(not isinstance(x,dict) for x in s) or [x.get('kind') for x in s]!=[x[1] for x in SCHEMA]:
        raise SyntaxErrorV020('invalid IR layout')
    # Reject tampered IR by recreating source and reparsing, exact fields.
    markers=['⊙','◆','○','!']
    source='\n'.join(f"{m} [{row['id']}] {row['kind']} "+' '.join(
        f'{k}={v}' for k,v in row.items() if k not in {'id','kind'})
        for m,row in zip(markers,s))
    if parse(source)!=doc:
        raise SyntaxErrorV020('IR roundtrip mismatch')
    adv,asset=s[1],s[2]
    verified=False
    if isinstance(trusted_context,dict):
        # The runtime does not allow document fields to claim their own host verification.
        verified = (trusted_context.get('cve')==adv['cve']
            and trusted_context.get('source_ref')==adv['source_ref']
            and trusted_context.get('asset_id')==asset['asset_id']
            and trusted_context.get('component')==asset['component']
            and trusted_context.get('version')==asset['version']
            and trusted_context.get('trusted') is True
            and trusted_context.get('inventory_fresh') is True
            and trusted_context.get('source_fresh') is True)
    gaps=[]
    if not verified: gaps.append('independent_source_and_inventory_unverified')
    if adv['source_state']!='verified': gaps.append('advisory_claim_not_verified')
    if asset['affected']=='unknown': gaps.append('affected_state_unknown')
    if asset['reachable']=='unknown': gaps.append('reachability_unknown')
    if asset['trust']=='unknown': gaps.append('trust_root_unknown')
    if asset['trust']=='revoked': gaps.append('trust_revoked')
    if not gaps and asset['affected']=='no':
        disposition='bounded_no_exposure_candidate'
    elif not gaps and asset['affected']=='yes' and asset['reachable']=='yes':
        disposition='affected_escalate_to_human'
    elif not gaps and asset['affected']=='yes' and asset['reachable']=='no':
        disposition='bounded_reachability_review'
    else:
        disposition='hold_unknown_or_untrusted'
    result={'cve':adv['cve'],'asset_id':asset['asset_id'],
        'disposition':disposition,'gaps':sorted(gaps),
        'trusted_context_matched':verified,
        'execution_allowed':False,'may_publish_safe_claim':False,
        'human_final_required':True,
        'warning':'A host-provided context is simulated input, not proof of authenticated production inventory.'}
    result['decision_digest']=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    return result


def run(source:str,trusted_context:dict[str,Any]|None=None)->dict[str,Any]:
    return evaluate(parse(source),trusted_context)

if __name__=='__main__':
    import argparse,sys
    parser=argparse.ArgumentParser()
    parser.add_argument('source',help='four-line .bridge fixture')
    parser.add_argument('--context',help='separate host context JSON; only synthetic tests')
    args=parser.parse_args()
    try:
        with open(args.source,encoding='utf-8') as f: raw=f.read()
        context=None
        if args.context:
            with open(args.context,encoding='utf-8') as f: context=json.load(f)
        print(json.dumps(run(raw,context),ensure_ascii=False,sort_keys=True,indent=2))
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(f'Bridge-0 security triage rejected: {exc}',file=sys.stderr)
        raise SystemExit(2)