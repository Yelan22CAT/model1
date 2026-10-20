// Generated from Bridge-0 v0.13. Do not hand-edit.
const tokens = ['nan','+inf','-inf','-0','+0','2.5','3.5','-2.5','-3.5'];

function decode(token) {
  if (token === 'nan') return Number.NaN;
  if (token === '+inf') return Number.POSITIVE_INFINITY;
  if (token === '-inf') return Number.NEGATIVE_INFINITY;
  if (token === '-0') return -0;
  if (token === '+0') return 0;
  return Number(token);
}

function classify(value) {
  if (Number.isNaN(value)) return { $binary64: 'nan' };
  if (value === Number.POSITIVE_INFINITY) return { $binary64: '+inf' };
  if (value === Number.NEGATIVE_INFINITY) return { $binary64: '-inf' };
  if (Object.is(value, -0)) return { $binary64: '-0' };
  if (Object.is(value, 0)) return { $binary64: '+0' };
  return { $binary64: value.toPrecision(17).replace(/(?:\.0+|(?:(\.[0-9]*?)0+))$/, '$1') };
}

function roundTiesToEven(value) {
  const floor = Math.floor(value);
  const fraction = value - floor;
  if (fraction < 0.5) return floor;
  if (fraction > 0.5) return floor + 1;
  return floor % 2 === 0 ? floor : floor + 1;
}

const exactInteger = (value) => ({ $exact_integer: String(value) });
const values = tokens.map((token) => [token, decode(token)]);
const classes = {};
const rounded = {};
for (const [token, value] of values) {
  classes[token] = classify(value);
  if (token.endsWith('.5')) rounded[token] = exactInteger(roundTiesToEven(value));
}
const result = { classes, rounded };
process.stdout.write(JSON.stringify(result) + '\n');
