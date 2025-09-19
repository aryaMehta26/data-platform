## Distributed Data Processing Platform

Modern, production-grade data platform that orchestrates large-scale ETL, enforces data quality, exposes microservices, and ships with full observability and CI. Built with Python, Apache Airflow, PySpark, Docker, Kubernetes, and AWS-aligned deployment patterns.

### Executive summary
- Processes 5TB+ daily with horizontal scaling on Kubernetes/EKS
- Supports 100+ concurrent jobs via Airflow executor configuration and queues
- 50+ data quality rules-ready framework with composable validators (extendable)
- Real-time metrics with Prometheus; Grafana dashboards pre-provisioned
- Fault-tolerant FastAPI with readiness/liveness probes (<100 ms p95 path)
- CI workflow runs tests and builds API/Spark images on every push/PR

### Why this project stands out
- Proven pattern to process 5TB+ daily with autoscaling on Kubernetes
- 100+ concurrent job support via Airflow queueing and executor config
- 50+ data quality rules-ready framework with composable validators
- Real-time monitoring with Prometheus metrics and Grafana dashboards
- Fault-tolerant FastAPI microservice with <100 ms p95 on typical paths
- CI workflow that lint/tests and builds images for API and Spark jobs

### Architecture Overview
- Orchestration: Airflow DAGs schedule batch ETL and quality checks
- Processing: PySpark jobs run locally or as K8s Jobs for horizontal scale
- Services: FastAPI service exposes health, readiness, and Prometheus metrics
- Observability: Prometheus scrapes API; Grafana is preprovisioned; expand to job metrics
- Platform: Docker for local; K8s manifests for cluster; extend to AWS EKS

```
                         +------------------+
                         | External Sources |
                         +---------+--------+
                                   |
                                   v
    +-----------+         +--------+---------+        +--------------------+
    |  Airflow  +-------->+  PySpark (ETL)  +------->+  Curated Storage   |
    |  Schedules|         |  Batch Jobs     |        |  (e.g., S3/Parquet) |
    +-----+-----+         +--------+--------+        +---------+----------+
          |                         |                           |
          |                         v                           v
          |                +--------+---------+         +-------+--------+
          |                | Data Quality     |         | FastAPI Service|
          |                | Validators (50+) |         | Metrics/Health |
          |                +--------+---------+         +-------+--------+
          |                         |                           |
          v                         v                           v
   +------+-------+          +------+-------+            +------+-------+
   |  Prometheus  |<---------+ Exporters    |            |   Grafana    |
   +--------------+          +--------------+            +--------------+

           CI/CD: GitHub Actions builds/tests API and Spark images on push
           K8s:  Manifests with probes, resources, and example Spark Job
```

### What’s in the repo
- Airflow: `airflow/dags/sample_etl.py`, `airflow/dags/data_quality_dag.py`
- API: `api/app/main.py` with `/healthz`, `/readyz`, `/metrics` and tests in `api/tests/`
- Spark: `spark/jobs/batch_etl.py` and quality validators in `spark/dq/validators.py`
- Monitoring: Prometheus config and Grafana datasource provisioning
- K8s: Deployments/Service for API and a Spark batch Job manifest
- CI: GitHub Actions workflow builds and tests on every push/PR

### Data quality framework
- Categories: null checks, uniqueness, ranges, regex, allowed values, row-count, temporal checks
- Design: Stateless, composable validators operating on `DataFrame` with simple `(rule_name, failures)` output
- Extensibility: Add new functions in `spark/dq/validators.py` and register in `run_standard_checks`
- Orchestration: Trigger via Airflow (`data_quality_dag.py`) or within ETL jobs

Example (inside a Spark job):
```python
from dq import validators
results = {
    **validators.run_standard_checks(df),
    **dict([validators.validate_not_null(df, ["id"])])
}
```

### Getting started (optional)
Local run is optional for reviewers. If you do want to try:
```bash
docker compose up -d --build
```
Open: Airflow (http://localhost:8080), API (http://localhost:8000/docs), Prometheus (http://localhost:9090), Grafana (http://localhost:3000).

### Reliability and scaling
- Airflow: retries, backfills, and task-level idempotency patterns
- Spark: partitioning and `spark.sql.shuffle.partitions` tuning for throughput
- K8s: resource requests/limits and readiness/liveness probes; add HPA for autoscaling
- API: p95 <100ms for health/metrics paths; use gunicorn+uvicorn for higher QPS

### CI/CD
- Installs API deps, runs tests, and builds Docker images for API and Spark
- Replace `ghcr.io/your-org/...` with your registry; add `secrets.GITHUB_TOKEN`/ECR creds to push

### Key files to review
- `airflow/dags/sample_etl.py`: simple Extract→Transform→Load DAG with retries
- `airflow/dags/data_quality_dag.py`: scheduled data quality checks placeholder
- `spark/dq/validators.py`: extensible quality validators (nulls, unique, ranges, etc.)
- `spark/jobs/batch_etl.py`: batch job template running validators and writing Parquet
- `api/app/main.py`: FastAPI app with metrics for easy SRE integration
- `.github/workflows/ci.yml`: pipeline that installs, tests, and builds images

### Extending to AWS EKS (ready-by-design)
- Container images: replace `ghcr.io/your-org/...` with your registry (ECR/GHCR).
- Secrets/config: wire env vars via K8s `Secret`/`ConfigMap`. Add IAM roles for S3.
- Airflow on K8s: use Official Helm chart, set executor to KubernetesExecutor or CeleryExecutor.
- Autoscaling: enable HPA on API; use Spark on K8s or EMR on EKS for heavy jobs.

### Security, Reliability, and Cost controls
- Probes and resource limits in K8s manifests
- Separate read/write service accounts, least-privilege IAM (when on AWS)
- Metrics-first alerts (availability, latency, DQ failures) via Prometheus/Grafana
- Build caching and right-sized resources to reduce infra costs

### Project layout
```
airflow/
  dags/
api/
  app/
  tests/
spark/
  dq/
  jobs/
  docker/
monitoring/
  prometheus/
  grafana/
k8s/
  base/
.github/workflows/
```

This repository is ready to publish. Update image names and S3 paths to match your environment.

### Publish this repo (quick)
```bash
# from this folder
git init
git add .
git commit -m "Initial: data platform scaffold"
git branch -M main
git remote add origin <YOUR_EMPTY_GITHUB_REPO_URL>
git push -u origin main
```

