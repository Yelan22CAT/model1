require 'json'
rows=JSON.parse(File.read(ARGV[0]))
def val(s)
 return [false,'transport'] unless s['transport_valid']
 return [false,'canonical'] unless s['canonical_valid']
 return [false,'schema'] unless s['schema_supported']
 return [false,'spec-generation'] unless s['spec_generation']=='spec-rc1'
 return [false,'signature'] unless s['signature_valid']
 return [false,'trust-anchor'] unless s['trust_anchor_current']
 return [false,'claim'] unless s['claim_state']=='SUPPORTED'
 return [false,'independence'] unless s['independent_clusters']>=s['required_independent_clusters']
 return [false,'confidence'] unless s['confidence_status']=='CALIBRATED'
 return [false,'risk-policy'] unless s['risk_policy_current']
 return [false,'decision'] unless s['decision']=='ACT'
 return [false,'review'] unless s['review_current']
 return [false,'authorization'] unless s['authorization_current']
 return [false,'assurance-context'] unless s['assurance_context_match']
 return [false,'dependency-graph'] unless s['dependency_graph_match']
 return [false,'plan'] unless s['plan_valid']
 return [false,'runtime'] unless s['runtime_attested']
 return [false,'broker'] unless s['broker_behavior_conformant']
 return [false,'effect-mediation'] unless s['effect_surface_mediated']
 return [false,'replay'] unless s['replay_fresh']
 return [false,'restore'] unless s['restore_generation_coherent']
 return [false,'trust-terminal'] unless s['trust_terminal_state']=='NORMAL'
 [true,'ok']
end
STDOUT.write(rows.map{|x| ok,r=val(x['state']); "#{x['id']}|#{ok ? 1 : 0}|#{r}"}.join("\n")+"\n")
