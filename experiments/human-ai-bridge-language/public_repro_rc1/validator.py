import json,sys
def val(s):
 if not s['transport_valid']: return False,'transport'
 if not s['canonical_valid']: return False,'canonical'
 if not s['schema_supported']: return False,'schema'
 if s['spec_generation']!='spec-rc1': return False,'spec-generation'
 if not s['signature_valid']: return False,'signature'
 if not s['trust_anchor_current']: return False,'trust-anchor'
 if s['claim_state']!='SUPPORTED': return False,'claim'
 if s['independent_clusters']<s['required_independent_clusters']: return False,'independence'
 if s['confidence_status']!='CALIBRATED': return False,'confidence'
 if not s['risk_policy_current']: return False,'risk-policy'
 if s['decision']!='ACT': return False,'decision'
 if not s['review_current']: return False,'review'
 if not s['authorization_current']: return False,'authorization'
 if not s['assurance_context_match']: return False,'assurance-context'
 if not s['dependency_graph_match']: return False,'dependency-graph'
 if not s['plan_valid']: return False,'plan'
 if not s['runtime_attested']: return False,'runtime'
 if not s['broker_behavior_conformant']: return False,'broker'
 if not s['effect_surface_mediated']: return False,'effect-mediation'
 if not s['replay_fresh']: return False,'replay'
 if not s['restore_generation_coherent']: return False,'restore'
 if s['trust_terminal_state']!='NORMAL': return False,'trust-terminal'
 return True,'ok'
for x in json.load(open(sys.argv[1])):
 ok,reason=val(x['state'])
 print(f"{x['id']}|{1 if ok else 0}|{reason}")
