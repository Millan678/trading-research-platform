#!/usr/bin/env python3
"""GitHub repo configuration script.
Requires GITHUB_TOKEN environment variable.
"""
import json
import urllib.request
import os
import sys

TOKEN = os.environ.get("GITHUB_TOKEN", "")
if not TOKEN:
    print("Error: Set GITHUB_TOKEN env var before running.")
    sys.exit(1)

REPO = "Millan678/trading-research-platform"
BASE = f"https://api.github.com/repos/{REPO}"

def api_call(method, endpoint, data=None):
    url = f"{BASE}/{endpoint}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        return {"error": err, "status": e.code}

# Labels
labels = [
    ("safety", "ff0000", "Safety enforcement"),
    ("research-only", "0052cc", "Research-only compliance"),
    ("determinism", "5319e7", "Determinism verification"),
    ("bridge", "0e8a16", "Bridge module issues"),
    ("documentation", "0075ca", "Documentation"),
    ("certification", "bfd4f2", "Certification issues"),
]

for name, color, desc in labels:
    r = api_call("POST", "labels", {"name": name, "color": color, "description": desc})
    status = r.get("name", r.get("error", "unknown")[:60])
    print(f"  Label '{name}': {status}")

# Milestone
r = api_call("POST", "milestones", {"title": "v1.0.0", "description": "Complete Research Platform (Phases 1-64)", "state": "closed"})
status = r.get("number", r.get("error", "unknown")[:60])
print(f"  Milestone v1.0.0: {status}")

print("\nGitHub configuration complete")
