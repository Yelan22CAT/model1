import copy, json, subprocess, tempfile, pathlib, sys

profile=json.load(open('DECISION_PROFILE_RC1.json'))
rows=json.load(open('corpus.json'))

def eval_profile(p,s):
    for g in p['ordered_gates']:
        x=s[g['field']]
        if g['op']=='eq': ok=(x==g['value'])
        elif g['op']=='gte_field': ok=(x>=s[g['value']])
        else: raise RuntimeError(g['op'])
        if not ok: return False,g['reason']
    return True,'ok'

# Directed one-negative-case-per-gate mutation kill test.
base={
 'transport_valid':True,'canonical_valid':True,'schema_supported':True,'spec_generation':'spec-rc1',
 'signature_valid':True,'trust_anchor_current':True,'claim_state':'SUPPORTED',
 'independent_clusters':2,'required_independent_clusters':2,'confidence_status':'CALIBRATED',
 'risk_policy_current':True,'decision':'ACT','review_current':True,'authorization_current':True,
 'assurance_context_match':True,'dependency_graph_match':True,'plan_valid':True,
 'runtime_attested':True,'broker_behavior_conformant':True,'effect_surface_mediated':True,
 'replay_fresh':True,'restore_generation_coherent':True,'trust_terminal_state':'NORMAL'
}

def invalidate(s,g):
    if g['op']=='gte_field':
        s[g['field']]=0
        s[g['value']]=2
        return
    v=g['value']
    if isinstance(v,bool): s[g['field']]=not v
    elif g['field']=='spec_generation': s[g['field']]='old-spec'
    elif g['field']=='claim_state': s[g['field']]='CONFLICT'
    elif g['field']=='confidence_status': s[g['field']]='UNAVAILABLE'
    elif g['field']=='decision': s[g['field']]='DEFER'
    elif g['field']=='trust_terminal_state': s[g['field']]='EXTERNAL_TRUST_BOOTSTRAP_REQUIRED'
    else: s[g['field']]='__invalid__'

killed=0
for i,g in enumerate(profile['ordered_gates']):
    s=copy.deepcopy(base)
    invalidate(s,g)
    expected=eval_profile(profile,s)
    mutant=copy.deepcopy(profile)
    mutant['ordered_gates'].pop(i)
    got=eval_profile(mutant,s)
    if expected!=got:
        killed+=1

print(json.dumps({'mutants':len(profile['ordered_gates']),'killed':killed}))
if killed!=len(profile['ordered_gates']):
    sys.exit(2)
