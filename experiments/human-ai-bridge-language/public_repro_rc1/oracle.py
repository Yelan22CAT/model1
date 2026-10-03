import json,sys
from pathlib import Path
SCHEMA=json.loads(Path(__file__).with_name('STATE_SCHEMA_RC1.json').read_text())
REQ=set(SCHEMA['state_required_fields']); ITEM_REQ=set(SCHEMA['item_required_fields']); MAX=SCHEMA['max_safe_integer']
def t_ok(v,t):
 if t=='boolean': return type(v) is bool
 if t=='string': return type(v) is str
 if t=='nonnegative_safe_integer_value':
  return type(v) in (int,float) and v==v and v not in (float('inf'),float('-inf')) and float(v).is_integer() and 0<=v<=MAX
 return False
def shape_ok(x):
 if type(x) is not dict or set(x)!=ITEM_REQ: return False
 if type(x['id']) is not int or not (0<=x['id']<=MAX): return False
 s=x['state']
 if type(s) is not dict or set(s)!=REQ: return False
 return all(t_ok(s[k],t) for k,t in SCHEMA['state_required_fields'].items())
profile=json.load(open(sys.argv[1],encoding='utf-8'))
rows=json.load(open(sys.argv[2],encoding='utf-8'))
if type(rows) is not list: raise SystemExit(2)
for item in rows:
 if not shape_ok(item):
  ident=item.get('id','?') if type(item) is dict else '?'
  print(f'{ident}|0|schema'); continue
 state=item['state']; result=True; reason='ok'
 for gate in profile['ordered_gates']:
  current=state[gate['field']]
  if gate['op']=='eq': passed=current==gate['value']
  elif gate['op']=='gte_field': passed=current>=state[gate['value']]
  else: passed=False
  if not passed:
   result=False; reason=gate['reason']; break
 print(str(item['id'])+'|'+('1' if result else '0')+'|'+reason)
