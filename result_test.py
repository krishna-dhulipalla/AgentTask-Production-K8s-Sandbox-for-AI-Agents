
import json
import os
import time

print("Running result test...")
os.makedirs("/workspace/artifacts", exist_ok=True)

result = {
    "status": "success",
    "score": 0.98,
    "data": ["foo", "bar"]
}

# Write to the Termination Message Path
with open("/workspace/artifacts/result.json", "w") as f:
    json.dump(result, f)

print("Result written to /workspace/artifacts/result.json")
print("Sleeping for 60 seconds to allow debugging...")
time.sleep(60)
