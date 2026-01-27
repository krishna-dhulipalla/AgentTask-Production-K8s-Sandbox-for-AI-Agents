# AgentTask Operator - Development & Setup Guide

This guide documents how to set up the development environment, run the operator, and use the CLI, based on the verified working setup.

## Prerequisites

- **Go** (v1.23+)
- **Docker** (Desktop or Engine)
- **Kind** (Kubernetes in Docker)
- **Kubectl**
- **Make**

## 1. Cluster Setup

Create a local Kubernetes cluster using Kind.

```bash
kind create cluster --name agenttask --image kindest/node:v1.32.2
```

Verify connectivity:

```bash
kubectl cluster-info --context kind-agenttask
kubectl get nodes
```

## 2. Install CRDs

Install the Custom Resource Definitions (CRDs) into the cluster.

```bash
make install
```

This generates the CRDs from the Go code and applies them to the cluster.

## 3. Run the Controller

You can run the controller locally (outside the cluster) for rapid development.

```bash
make run
```

_Keep this terminal open._ The controller logs will appear here.

## 4. Build and Use `agentctl`

In a new terminal, build the CLI tool.

### Build

```bash
go mod tidy
go build -o agentctl cmd/agentctl/main.go
```

### Usage

**Run a Task**:
Create a python file (e.g., `hello.py`):

```python
import time
print("Hello from AgentTask!")
time.sleep(5)
print("Task Complete.")
```

Submit it:

```bash
./agentctl run hello.py
```

**List Tasks**:

```bash
./agentctl list
```

_Expected Output:_

```text
NAME          PHASE       AGE   POD
hello-xxxxx   Running     5s    hello-xxxxx-pod
```

**Get Logs**:

```bash
./agentctl logs <task-name>
```

**Delete Task**:

```bash
./agentctl delete <task-name>
```

## Troubleshooting

- **CreateContainerConfigError**: Usually means a SecurityContext issue. Ensure the controller is running the latest version which sets `RunAsUser: 1000`.
- **ImagePullBackOff**: Ensure `python:3.11-slim` can be pulled (check internet connection).
