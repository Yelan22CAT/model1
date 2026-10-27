#!/usr/bin/env node
"use strict";
// Experimental synthetic admission policy v2. NOT the Bridge-0 parser,
// normative grammar, RC1 conformance or permission authority.
function admit(x) {
  if (!x || typeof x !== "object" || Array.isArray(x)) return false;
  if (x.claim === "verified" && x.proof !== true) return false; // illustrative proof flag only
  if (x.autoJoin === true && x.sameTransport !== true) return false;
  if (x.assertIndependent !== undefined) {
    if (![x.total,x.unique,x.assertIndependent].every(Number.isSafeInteger)) return false;
    if (x.total <= 0 || x.unique <= 0 || x.unique > x.total ||
        x.assertIndependent < 1 || x.assertIndependent > x.unique) return false;
  }
  if (typeof x.page === "string" && x.page.toUpperCase() === "I" && x.crc8Required === true) return false;
  if (x.write === true && x.approved !== true) return false;
  return true;
}
const cases=[
["verified requires evidence",{claim:"verified",proof:false},false],
["verified with proof",{claim:"verified",proof:true},true],
["candidate without proof",{claim:"candidate",proof:false},true],
["unknown stays unknown",{claim:"unknown",proof:false},true],
["isolate unrelated transports",{sameTransport:false,autoJoin:true},false],
["cross compare without joining",{sameTransport:false,autoJoin:false},true],
["repeated samples are not independent",{total:4349,unique:14,assertIndependent:4349},false],
["unique counts respected",{total:4349,unique:14,assertIndependent:14},true],
["I page not forced CRC8",{page:"I",crc8Required:true},false],
["A page with CRC8",{page:"A",crc8Required:true},true],
["read-only analysis",{tool:"capture-analysis",write:false},true],
["unauthorized write",{tool:"device-bus",write:true,approved:false},false],
["string is not a verified proof",{claim:"verified",proof:"invented"},false],
["negative unique count",{total:100,unique:-1,assertIndependent:0},false],
["claimed independent exceeds unique",{total:4,unique:3,assertIndependent:5},false],
["negative independent count",{total:100,unique:14,assertIndependent:-2},false],
["zero unique count",{total:100,unique:0,assertIndependent:0},false],
["missing sameTransport fails auto join",{autoJoin:true},false],
["missing approval fails write",{write:true},false],
["lowercase I alias cannot bypass",{page:"i",crc8Required:true},false],
["explicit proof flag admitted",{claim:"verified",proof:true},true],
["explicit read-only admitted",{write:false},true]
];
let passed=0;
for(const [name,input,expected] of cases) {
  const actual=admit(input), ok=actual===expected;
  if(ok) passed++;
  console.log((ok?"PASS ":"FAIL ")+name);
}
console.log(JSON.stringify({scope:"synthetic policy-v2 regression; not Bridge conformance",passed,total:cases.length}));
if(passed!==cases.length) process.exitCode=1;
