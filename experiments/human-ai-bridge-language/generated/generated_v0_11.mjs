// Generated from Bridge-0 v0.11. Do not hand-edit.
const values = [2,3,5,7,11,13];
const result = {
  count: values.length,
  max: Math.max(...values),
  min: Math.min(...values),
  sum: values.reduce((a, b) => a + b, 0),
};
process.stdout.write(JSON.stringify(result) + '\n');
