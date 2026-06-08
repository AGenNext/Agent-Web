# Deploy — registry agent

The registry agent's HTTP surface, containerized and Kubernetes-ready.

> ⚠️ **Secrets:** never bake secrets into the image or manifests. Inject via a
> Kubernetes `Secret` + `envFrom`. **Rotate any secret ever pasted into a chat,
> logged, or committed.**

## Local (no cluster — verified working)

```bash
python -m agentweb.http_server          # serves on :8080
curl localhost:8080/healthz             # {"status":"ok"}
curl -X POST localhost:8080/ -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Container

```bash
docker build -t agentweb-registry:latest .
docker run -p 8080:8080 agentweb-registry:latest
```

## Kubernetes

```bash
docker build -t agentweb-registry:latest .
# load/push the image into your cluster's registry, then:
kubectl apply -f deploy/k8s/registry.yaml
kubectl port-forward svc/agentweb-registry 8080:80
curl localhost:8080/healthz
```

- **Edge:** k0s / MicroK8s (single-binary, conformant).
- **Network / datacenter:** full k8s.

The manifest runs as **non-root**, read-only rootfs, all capabilities dropped,
with health/readiness probes — least privilege by default.
