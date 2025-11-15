from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    "owner": "data-platform",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def extract(**context):
    return [{"id": i, "value": i * 2} for i in range(10)]


def transform(ti, **context):
    records = ti.xcom_pull(task_ids="extract")
    return [r for r in records if r["id"] % 2 == 0]


def load(ti, **context):
    records = ti.xcom_pull(task_ids="transform")
    print(f"Loaded {len(records)} records")


with DAG(
    dag_id="sample_etl",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["example", "etl"],
) as dag:
    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load", python_callable=load)

    t1 >> t2 >> t3


