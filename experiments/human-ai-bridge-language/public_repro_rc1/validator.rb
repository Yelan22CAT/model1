require 'json'
schema=JSON.parse(File.read(File.join(__dir__,'STATE_SCHEMA_RC1.json')))
REQ=schema['state_required_fields'].keys.sort.freeze
ITEM_REQ=schema['item_required_fields'].sort.freeze
MAX=schema['max_safe_integer']
def exact_keys(o, keys); o.is_a?(Hash) && o.keys.sort==keys; end
def t_ok(v,t,max)
 return (v==true || v==false) if t=='boolean'
 return v.is_a?(String) if t=='string'
 return ((v.is_a?(Integer)) || (v.is_a?(Float) && v.finite? && v==v.to_i)) && v>=0 && v<=max if t=='nonnegative_safe_integer_value'
 false
end
def shape_ok(x,schema,max)
 return false unless exact_keys(x,ITEM_REQ)
 return false unless x['id'].is_a?(Integer) && x['id']>=0 && x['id']<=max
 s=x['state']; return false unless exact_keys(s,REQ)
 schema['state_required_fields'].all?{|k,t| t_ok(s[k],t,max)}
end
def val(s)
 return [false,'transport'] unless s['transport_valid']; return [false,'canonical'] unless s['canonical_valid']; return [false,'schema'] unless s['schema_supported']; return [false,'spec-generation'] unless s['spec_generation']=='spec-rc1'; return [false,'signature'] unless s['signature_valid']; return [false,'trust-anchor'] unless s['trust_anchor_current']; return [false,'claim'] unless s['claim_state']=='SUPPORTED'; return [false,'independence'] unless s['independent_clusters']>=s['required_independent_clusters']; return [false,'confidence'] unless s['confidence_status']=='CALIBRATED'; return [false,'risk-policy'] unless s['risk_policy_current']; return [false,'decision'] unless s['decision']=='ACT'; return [false,'review'] unless s['review_current']; return [false,'authorization'] unless s['authorization_current']; return [false,'assurance-context'] unless s['assurance_context_match']; return [false,'dependency-graph'] unless s['dependency_graph_match']; return [false,'plan'] unless s['plan_valid']; return [false,'runtime'] unless s['runtime_attested']; return [false,'broker'] unless s['broker_behavior_conformant']; return [false,'effect-mediation'] unless s['effect_surface_mediated']; return [false,'replay'] unless s['replay_fresh']; return [false,'restore'] unless s['restore_generation_coherent']; return [false,'trust-terminal'] unless s['trust_terminal_state']=='NORMAL'; [true,'ok']
end
rows=JSON.parse(File.read(ARGV[0])); exit 2 unless rows.is_a?(Array)
out=rows.map do |x|
 if !shape_ok(x,schema,MAX); "#{x.is_a?(Hash) && x.key?('id') ? x['id'] : '?'}|0|schema" else ok,r=val(x['state']); "#{x['id']}|#{ok ? 1 : 0}|#{r}" end
end
STDOUT.write(out.join("\n")+"\n")
