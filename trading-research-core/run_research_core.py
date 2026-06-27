#!/usr/bin/env python3
"""Run Phase 62 — Unified Autonomous Scientific Research Foundation."""
import sys, os, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from research_core import ResearchCorePlatform

output_dir = sys.argv[1] if len(sys.argv) > 1 else "/tmp/research_core_demo"
os.makedirs(output_dir, exist_ok=True)

platform = ResearchCorePlatform(output_dir, seed=0)
result = platform.run()

print("Phase 62 Research Core Platform - COMPLETE")
for key, value in sorted(result.items()):
    if key == "metrics":
        print(f"  metrics:")
        for mk, mv in value.items():
            print(f"    {mk}: {mv}")
    else:
        print(f"  {key}: {value}")
