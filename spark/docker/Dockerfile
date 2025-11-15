FROM bitnami/spark:3.5.1

USER root
WORKDIR /opt/jobs

# Copy DQ validators and jobs (build context should be from spark/ directory)
COPY dq /opt/jobs/dq
COPY jobs /opt/jobs/jobs

# Set PYTHONPATH so imports work
ENV PYTHONPATH=/opt/jobs:$PYTHONPATH

USER 1001

ENTRYPOINT ["/opt/bitnami/scripts/spark/bin/spark-submit", \
  "--master", "local[*]", \
  "/opt/jobs/jobs/batch_etl.py"]

