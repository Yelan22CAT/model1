import hashlib, json, platform, subprocess, sys
from pathlib import Path

EXPECTED_CORPUS="f9d47a0dd93bc7d8bc5171dab1465fa11cf1d18794d66f8ffc56c4102ac75f04"
EXPECTED_OUTPUT="6e91757ca0921a94ac4300fcee1918f85d862039354da1b542560536083136bf"

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

actual_corpus=sha("corpus.json")
actual_output=sha("python.out")

env={
    "python": platform.python_version(),
    "node": subprocess.check_output(["node","--version"], text=True).strip(),
    "ruby": subprocess.check_output(["ruby","--version"], text=True).strip(),
    "platform": platform.platform(),
}
print(json.dumps({
    "environment":env,
    "corpus_sha256":actual_corpus,
    "output_sha256":actual_output,
    "corpus_match":actual_corpus==EXPECTED_CORPUS,
    "output_match":actual_output==EXPECTED_OUTPUT,
},indent=2))

if actual_corpus!=EXPECTED_CORPUS or actual_output!=EXPECTED_OUTPUT:
    sys.exit(2)
