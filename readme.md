# DevOps Worker Sample

This project is a simple **Worker** that fetches URLs from a **Redis queue**, processes them, and exposes results as **Prometheus metrics**.  
It also uses **Postgres** for data storage.

---

## ⚙️ 1. Local Setup (Docker Compose)

### Build Worker Image
```bash
docker build -f Dockerfile -t devops-worker-sample:latest .
```

you can checkc image

```bash
docker images | grep devops-worker-sample
```

## Run Enviorment
```bash
docker compose up --build -d
```

### Check worker logs
```bash
docker compose logs -f worker
```

## 🔍 2. Test Services in Docker

### Healthcheck

```bash
curl http://localhost:9000/healthz
```
### Metrics
```bash
curl http://localhost:9000/metrics
```
## 🗃️ 3. Test Redis

Enter redis-cli
```bash 
docker exec -it dev_redis redis-cli
```
Add url
```bash
LPUSH urls https://example.com
```
Check metrics again
```bash
curl http://localhost:9000/metrics
```
Expected --> crawler_fetch_total and crawler_success_total increas

## 🛢️ 4. Test Postgres
Enter database
```bash
docker exec -it dev_postgres psql -U dev -d devdb
```
## ☸️ 5. Kubernetes Deployment
Create namespace
```bash
kubectl create namespace devops-sample
```
**Deploy Redis & Postgres**
```bash
kubectl apply -f k8s/postgres-deployment.yaml -n devops-sample
kubectl apply -f k8s/redis-deployment.yaml -n devops-sample
```
**Deploy Worker**
```bash
kubectl apply -f k8s/deployment-worker.yaml -n devops-sample
kubectl apply -f k8s/service-worker.yaml -n devops-sample
```

**Check pods**
```bash
kubectl get pods -n devops-sample
```
**Check logs**
```bash
kubectl logs -f <worker-pod-name> -n devops-sample
```
**Access Service**
```bash
kubectl port-forward svc/worker-service 9001:8000 -n devops-sample
```
Then
```bash
curl http://localhost:9001/healthz
curl http://localhost:9001/metrics
```
## 🕹️ 6. CAPTCHA Simulation
Add url
```bash
LPUSH urls http://invalid-url.test
```
Check metrics
```bash
curl http://localhost:8080/metrics
```
```crawler_error_total``` should increase

Worker logs will show: ***CAPTCHA detected***, ***quarantining worker***

[Check Runbook]([https://github.com/aria3211/DevOps/blob/main/RUNBOOK.md](https://github.com/aria3211/DevOps/blob/main/Runbook.md))
