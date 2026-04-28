#!/bin/bash

# Merge parallel group outputs and update history.json (source of truth)

set -e

echo "Merging results from all groups..."

python3 << 'PYSCRIPT'
import json
import os

# Collect results from all group files
all_models = []
timestamp = None
prompt = None

for group_file in ["results-group1.json", "results-group2.json"]:
    if os.path.exists(group_file):
        with open(group_file, "r") as f:
            data = json.load(f)
            all_models.extend(data.get("models", []))
            if not timestamp:
                timestamp = data.get("timestamp")
                prompt = data.get("prompt")

if not all_models:
    print("No results found!")
    exit(1)

# Calculate summary
success_count = sum(1 for m in all_models if m.get('success'))
total_count = len(all_models)
fastest_model = "N/A"
fastest_time = 0

successful = [m for m in all_models if m.get('success')]
if successful:
    fastest = min(successful, key=lambda x: x.get('responseTime', float('inf')))
    fastest_model = fastest.get('model', 'N/A')
    fastest_time = fastest.get('responseTime', 0)

# Create merged result
merged_result = {
    "timestamp": timestamp,
    "prompt": prompt,
    "models": all_models,
    "summary": {
        "successCount": success_count,
        "totalModels": total_count,
        "fastestModel": fastest_model,
        "fastestTime": fastest_time
    }
}

# Update history.json
if os.path.exists("../history.json"):
    with open("../history.json", "r") as f:
        history = json.load(f)
else:
    history = {"runs": []}

history['runs'].insert(0, merged_result)
history['runs'] = history['runs'][:720]

with open("../history.json", "w") as f:
    json.dump(history, f, indent=2)

print(f"✓ Updated history.json with new run")

# Clean up group files
for group_file in ["results-group1.json", "results-group2.json"]:
    if os.path.exists(group_file):
        os.remove(group_file)

print("✓ Cleaned up temporary group files")
PYSCRIPT
