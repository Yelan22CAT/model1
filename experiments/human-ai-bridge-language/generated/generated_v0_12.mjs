// Generated from Bridge-0 v0.12. Do not hand-edit.
const values = [9007199254740991n,9007199254740993n,-9007199254740995n,18446744073709551617n];
const exact = (value) => ({ $exact_integer: value.toString() });
const sum = values.reduce((a, b) => a + b, 0n);
const max = values.reduce((a, b) => (a > b ? a : b));
const min = values.reduce((a, b) => (a < b ? a : b));
const result = {
  count: exact(BigInt(values.length)),
  max: exact(max),
  min: exact(min),
  sum: exact(sum),
};
process.stdout.write(JSON.stringify(result) + '\n');
