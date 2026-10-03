import hashlib, json, platform, subprocess, sys
from pathlib import Path

EXPECTED_CORPUS="0dcf5bf318fc8e1988a03267c3b35ba9764130a3e5e8104f7ef1593d0ef35fa5"
EXPECTED_OUTPUT="8a3d911a24fd018ef791314d5bba06d2b0fe85e7f30fb6e2dc117fcc40f1bcab"

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
