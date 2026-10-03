import hashlib, json, sys
from pathlib import Path

SEED="20261002"
N=256
BASE={
 'transport_valid':True,'canonical_valid':True,'schema_supported':True,'spec_generation':'spec-rc1',
 'signature_valid':True,'trust_anchor_current':True,'claim_state':'SUPPORTED',
 'independent_clusters':2,'required_independent_clusters':2,'confidence_status':'CALIBRATED',
 'risk_policy_current':True,'decision':'ACT','review_current':True,'authorization_current':True,
 'assurance_context_match':True,'dependency_graph_match':True,'plan_valid':True,
 'runtime_attested':True,'broker_behavior_conformant':True,'effect_surface_mediated':True,
 'replay_fresh':True,'restore_generation_coherent':True,'trust_terminal_state':'NORMAL'
}
MUTS=[
 ('transport_valid',False),('canonical_valid',False),('schema_supported',False),('spec_generation','old-spec'),
 ('signature_valid',False),('trust_anchor_current',False),('claim_state','CONFLICT'),('independent_clusters',1),
 ('confidence_status','UNAVAILABLE'),('risk_policy_current',False),('decision','DEFER'),('review_current',False),
 ('authorization_current',False),('assurance_context_match',False),('dependency_graph_match',False),('plan_valid',False),
 ('runtime_attested',False),('broker_behavior_conformant',False),('effect_surface_mediated',False),('replay_fresh',False),
 ('restore_generation_coherent',False),('trust_terminal_state','EXTERNAL_TRUST_BOOTSTRAP_REQUIRED')
]

class PRNG:
    def __init__(self, seed):
        self.seed=seed
        self.counter=0
    def u64(self):
        raw=(self.seed+":"+str(self.counter)).encode("utf-8")
        self.counter+=1
        return int.from_bytes(hashlib.sha256(raw).digest()[:8],"big")
    def below(self,n):
        return self.u64()%n

r=PRNG(SEED)
rows=[]
for i in range(N):
    s=dict(BASE)
    x=r.below(100)
    k=0 if x<20 else 1 if x<65 else 2 if x<90 else 3
    pool=list(range(len(MUTS)))
    picks=[]
    for _ in range(k):
        j=r.below(len(pool))
        picks.append(pool.pop(j))
    for idx in picks:
        f,v=MUTS[idx]
        s[f]=v
    rows.append({"id":i,"state":s})

out=Path(sys.argv[1] if len(sys.argv)>1 else "corpus.json")
out.write_text(json.dumps(rows,separators=(",",":")))
