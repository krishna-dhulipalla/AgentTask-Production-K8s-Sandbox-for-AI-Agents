# AgentTask Operator

A Kubernetes Operator for managing the lifecycle of ephemeral, secure, and isolated agentic tasks.

It provides a higher-level abstraction (`AgentTask`) over bare Pods, adding robust lifecycle management, security hardening, and ease of use for running AI agents or arbitrary code snippets.

## Features

### 🛡️ Secure by Design

- **Rootless Execution**: Tasks run as non-root user (UID 1000) by default.
- **Network Isolation**: Every task gets a default-deny NetworkPolicy, blocking all ingress and egress traffic.
- **Hardened Sandbox**: Read-only filesystem, specific capability drops, and Seccomp profiles.
- **Validation Webhooks**: Rejects invalid configurations (e.g., disallowed runtime profiles or dangerous timeouts) before they reach the cluster.

### ⚡ Lifecycle Management

- **Timeouts**: Built-in timeout enforcement to prevent runaway processes.
- **Cancellation**: Support for active cancellation of running tasks.
- **Result Capture**: Structured JSON results automatically extracted from the execution.
- **Failure Propagation**: Detailed failure reasons and exit codes propagated to the Task status.

### 🛠️ Developer Experience

- **Custom Resource Definition (CRD)**: Declarative API for defining tasks.
- **`agentctl` CLI**: A dedicated command-line tool to run, list, log, and manage tasks without writing YAML.

## Getting Started

### Prerequisites

- Kubernetes Cluster (v1.23+)
- `kubectl` installed and configured
- `cert-manager` (required for validation webhooks)

### Installation

1. **Install cert-manager** (if not already present):

   ```bash
   kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.17.0/cert-manager.yaml
   ```

2. **Deploy the Operator**:

   ```bash
   # Clone the repository
   git clone https://github.com/your-org/agenttask-operator.git
   cd agenttask-operator

   # Install CRDs
   make install

   # Build and Deploy (requires Docker)
   make docker-build IMG=controller:latest
   kind load docker-image controller:latest --name agenttask # If using Kind
   make deploy IMG=controller:latest
   ```

## Usage (CLI)

The `agentctl` tool is the easiest way to interact with the system.

### Build CLI

```bash
go build -o agentctl cmd/agentctl/main.go
```

### Run a Task

Create a python script `hello.py`:

```python
print("Hello from the secure sandbox!")
```

Run it:

```bash
./agentctl run hello.py --profile python3.11
```

### Manage Tasks

```bash
# List all tasks
./agentctl list

# Get logs
./agentctl logs hello-xxxxx

# Delete a task
./agentctl delete hello-xxxxx
```

## Usage (YAML)

You can also create tasks using standard Kubernetes YAML:

```yaml
apiVersion: execution.agenttask.io/v1alpha1
kind: AgentTask
metadata:
  name: my-task
spec:
  runtimeProfile: python3.11
  timeoutSeconds: 300
  code:
    source: |
      import os
      print(f"Running as user: {os.getuid()}")
  resources:
    limits:
      cpu: "500m"
      memory: "128Mi"
```

## Contributing

See [Development Guide](docs/setup_guide.md) for detailed setup and verification steps.

## License

Copyright 2026 AgentTask Authors.
Licensed under the Apache License, Version 2.0.
