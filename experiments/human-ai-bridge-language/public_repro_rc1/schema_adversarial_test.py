import copy,json,random,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE=json.loads((ROOT/'CORPUS_PROFILE_RC1.json').read_text())['base']
PY=sys.executable
CMDS=[
 [PY,'validator.py'],
 ['node','validator.js'],
 ['ruby','validator.rb'],
 [PY,'oracle.py','DECISION_PROFILE_RC1.json'],
]
def run_all(path):
 outs=[]
 for cmd in CMDS:
  p=subprocess.run(cmd+[str(path)],cwd=ROOT,text=True,capture_output=True)
  if p.returncode!=0:
   raise RuntimeError(f'{cmd} rc={p.returncode} stderr={p.stderr}')
  outs.append(p.stdout)
 if len(set(outs))!=1:
  raise AssertionError('cross-runtime/oracle divergence')
 return outs[0]
def item(i,mut=None,top=None):
 s=copy.deepcopy(BASE)
 if mut: s.update(mut)
 x={'id':i,'state':s}
 if top: x.update(top)
 return x
with tempfile.TemporaryDirectory() as td:
 td=Path(td)
 directed=[
  item(0),
  item(1,{'authorization_current':'false'}),
  item(2,{'unexpected_privilege':'ACT'}),
  item(3,{'independent_clusters':9007199254740992,'required_independent_clusters':9007199254740993}),
  item(4,{'independent_clusters':True}),
  item(5,{'independent_clusters':2.5}),
  item(6,{'independent_clusters':2.0,'required_independent_clusters':2.0}),
  item(7,top={'unexpected_top':True}),
  item(8),
 ]
 del directed[-1]['state']['review_current']
 dpath=td/'directed.json'; dpath.write_text(json.dumps(directed,separators=(',',':')))
 expected='\n'.join([
  '0|1|ok','1|0|schema','2|0|schema','3|0|schema','4|0|schema','5|0|schema','6|1|ok','7|0|schema','8|0|schema'
 ])+'\n'
 got=run_all(dpath)
 if got!=expected: raise AssertionError('directed schema regression')
 lex=[item(9,{'independent_clusters':2.0,'required_independent_clusters':2.0})]
 raw=json.dumps(lex,separators=(',',':')).replace('"independent_clusters":2.0','"independent_clusters":2e0',1)
 lpath=td/'lexeme.json'; lpath.write_text(raw)
 if run_all(lpath)!='9|1|ok\n': raise AssertionError('integer-valued numeric lexeme regression')
 r=random.Random(149)
 rows=[]; expected_lines=[]
 bool_fields=[k for k,v in BASE.items() if type(v) is bool]
 for i in range(5000):
  s=copy.deepcopy(BASE); mode=r.randrange(6); ok=False
  if mode==0:
   s[r.choice(bool_fields)]=r.choice(['false','true',0,1,None,[],{}])
  elif mode==1:
   s['unexpected_'+str(i)]=r.choice([True,'ACT',1])
  elif mode==2:
   s['independent_clusters']=9007199254740992+r.randrange(1000)
  elif mode==3:
   s['required_independent_clusters']=9007199254740992+r.randrange(1000)
  elif mode==4:
   s['independent_clusters']=r.choice([True,False,'2',None,2.5])
  else:
   s['independent_clusters']=2.0; s['required_independent_clusters']=2.0; ok=True
  rows.append({'id':1000+i,'state':s})
  expected_lines.append(f'{1000+i}|{1 if ok else 0}|{"ok" if ok else "schema"}')
 fpath=td/'fuzz.json'; fpath.write_text(json.dumps(rows,separators=(',',':')))
 got=run_all(fpath)
 expected='\n'.join(expected_lines)+'\n'
 if got!=expected: raise AssertionError('fuzz schema regression')
print(json.dumps({'directed_cases':9,'numeric_lexeme_cases':1,'fuzz_cases':5000,'cross_runtime_oracle_match':True,'false_accepts':0,'false_rejects':0},sort_keys=True))
