const fs=require('fs');
const rows=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
function val(s){
 if(!s.transport_valid)return [false,'transport'];
 if(!s.canonical_valid)return [false,'canonical'];
 if(!s.schema_supported)return [false,'schema'];
 if(s.spec_generation!=='spec-rc1')return [false,'spec-generation'];
 if(!s.signature_valid)return [false,'signature'];
 if(!s.trust_anchor_current)return [false,'trust-anchor'];
 if(s.claim_state!=='SUPPORTED')return [false,'claim'];
 if(s.independent_clusters<s.required_independent_clusters)return [false,'independence'];
 if(s.confidence_status!=='CALIBRATED')return [false,'confidence'];
 if(!s.risk_policy_current)return [false,'risk-policy'];
 if(s.decision!=='ACT')return [false,'decision'];
 if(!s.review_current)return [false,'review'];
 if(!s.authorization_current)return [false,'authorization'];
 if(!s.assurance_context_match)return [false,'assurance-context'];
 if(!s.dependency_graph_match)return [false,'dependency-graph'];
 if(!s.plan_valid)return [false,'plan'];
 if(!s.runtime_attested)return [false,'runtime'];
 if(!s.broker_behavior_conformant)return [false,'broker'];
 if(!s.effect_surface_mediated)return [false,'effect-mediation'];
 if(!s.replay_fresh)return [false,'replay'];
 if(!s.restore_generation_coherent)return [false,'restore'];
 if(s.trust_terminal_state!=='NORMAL')return [false,'trust-terminal'];
 return [true,'ok'];
}
let out='';
for(const x of rows){const [ok,r]=val(x.state);out+=`${x.id}|${ok?1:0}|${r}\n`;}
process.stdout.write(out);
