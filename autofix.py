import os
import json
import urllib.request
import urllib.error

with open("test_output.txt") as f:
    test_output = f.read()

with open("todo.py") as f:
    broken_code = f.read()

prompt = f"""You are an AI code repair tool.

A pytest test suite has failed. Your job is to fix the Python source file so all tests pass.

## Broken source file (todo.py)
```python
{broken_code}
```

## Pytest failure output
```
{test_output}
```

Return ONLY the corrected Python source code — no explanation, no markdown fences, no extra text.
The very first character of your response must be the first character of the Python file."""

payload = json.dumps({
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0,
}).encode()

req = urllib.request.Request(
    "https://api.openai.com/v1/chat/completions",
    data=payload,
    headers={
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    },
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
except urllib.error.HTTPError as e:
    print(f"OpenAI API error: {e.code} {e.read().decode()}")
    raise

fixed = result["choices"][0]["message"]["content"].strip()

# Strip accidental markdown code fences if the model added them
if fixed.startswith("```"):
    lines = fixed.splitlines()
    fixed = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

with open("todo.py", "w") as f:
    f.write(fixed)

print("autofix.py: fix written to todo.py")
print("─" * 40)
print(fixed)
