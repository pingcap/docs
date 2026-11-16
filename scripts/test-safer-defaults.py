"""Regression checks for repository and documentation defaults."""

import ast
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


ci_workflow = (ROOT / ".github/workflows/ci.yaml").read_text()
install_commands = [
    line.split("#", 1)[0]
    for line in ci_workflow.splitlines()
    if re.search(r"\bnpm\s+ci\b", line.split("#", 1)[0])
]
assert install_commands
assert all(
    re.search(r"(?:^|\s)--ignore-scripts(?:=true)?(?:\s|$)", command)
    for command in install_commands
)
assert all("--include=dev" in command for command in install_commands)

deployment = (ROOT / "check-before-deployment.md").read_text()
permission_commands = [
    line.strip()
    for line in deployment.splitlines()
    if re.search(r"\bchmod\b", line)
]
unsafe_permission_patterns = (
    re.compile(r"\bchmod\b[^\n]*\b[0-7]{2,3}[2367]\b"),
    re.compile(r"\b(?:a|ugo|go|g|o)[+=][^\s,]*w"),
)
assert not any(
    pattern.search(command)
    for command in permission_commands
    for pattern in unsafe_permission_patterns
)
assert "sudo install -d -o tidb -g tidb -m 700" in deployment
assert "sudo chmod -R u=rwX,go=" in deployment

dm_quick_start = (ROOT / "dm/quick-start-with-dm.md").read_text()
assert "--nogpgcheck" not in dm_quick_start
assert "Do not bypass the error by disabling signature verification." in dm_quick_start

vector_quick_start = (ROOT / "ai/vector-search-get-started-using-python.md").read_text()
python_blocks = re.findall(r"```python\s*\n(.*?)```", vector_quick_start, re.DOTALL)
model_calls = []
for block in python_blocks:
    tree = ast.parse(block)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        if isinstance(function, ast.Name):
            function_name = function.id
        elif isinstance(function, ast.Attribute):
            function_name = function.attr
        else:
            continue
        if function_name == "SentenceTransformer":
            model_calls.append(node)

assert model_calls
for call in model_calls:
    trust_remote_code = next(
        (keyword.value for keyword in call.keywords if keyword.arg == "trust_remote_code"),
        None,
    )
    assert isinstance(trust_remote_code, ast.Constant)
    assert trust_remote_code.value is False

print("safer default checks passed")
