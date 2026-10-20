import hashlib, json, sys
from pathlib import Path

PROFILE_PATH=Path(__file__).with_name("CORPUS_PROFILE_RC1.json")
PROFILE=json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
SEED=PROFILE["seed"]
N=PROFILE["cases"]
BASE=PROFILE["base"]
MUTS=PROFILE["mutations"]
TH=PROFILE["k_thresholds"]

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
    k=0 if x<TH["0"] else 1 if x<TH["1"] else 2 if x<TH["2"] else 3
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
