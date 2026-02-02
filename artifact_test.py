
import os
import time

print("Starting artifact test...")
os.makedirs("/workspace/artifacts", exist_ok=True)
with open("/workspace/artifacts/test-artifact.txt", "w") as f:
    f.write("This is a test artifact captured by the sidecar.")
print("Artifact written to /workspace/artifacts/test-artifact.txt")
time.sleep(10) # Give sidecar time to see it
print("Done.")
