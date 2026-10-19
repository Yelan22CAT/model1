#!/usr/bin/env node
"use strict";
// Experimental bridge-adjacent evidence-admission test, NOT Bridge-0 grammar, parser,
// normative conformance, baseline or a substitute for the protected RC1 suite.
function admit(x) {
  if (x.claim === "verified" && !x.proof) return false;
  if (x.autoJoin && !x.sameTransport) return false;
  if (x.assertIndependent !== undefined && x.assertIndependent > x.unique) return false;
  if (x.page === "I" && x.crc8Required) return false;
  if (x.write && !x.approved) return false;
  return true;
}
const cases = [
  ["verified requires evidence",{claim:"verified",proof:false},false],
  ["verified with proof",{claim:"verified",proof:true},true],
  ["candidate without proof",{claim:"candidate",proof:false},true],
  ["unknown stays unknown",{claim:"unknown",proof:false},true],
  ["isolate unrelated transports",{sameTransport:false,autoJoin:true},false],
  ["cross compare with explicit provenance",{sameTransport:false,autoJoin:false},true],
  ["count effective samples",{total:4349,unique:14,assertIndependent:4349},false],
  ["count unique samples",{total:4349,unique:14,assertIndependent:14},true],
  ["I frame not forced CRC8",{page:"I",crc8Required:true},false],
  ["A page CRC8",{page:"A",crc8Required:true},true],
  ["read-only analysis",{tool:"capture-analysis",write:false},true],
  ["unauthorized device write",{tool:"device-bus",write:true,approved:false},false]
];
let passed = 0;
for (const [name,input,expected] of cases) {
  const actual = admit(input);
  const ok = actual === expected;
  if (ok) passed++;
  console.log((ok ? "PASS " : "FAIL ") + name);
}
console.log(JSON.stringify({scope:"synthetic non-normative evidence admission",passed,total:cases.length}));
if (passed !== cases.length) process.exitCode = 1;
