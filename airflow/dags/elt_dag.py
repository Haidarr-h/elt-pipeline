from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
import subprocess
# from airflow.operators.docker import DockerOperator
# from airflow.operators.python_operators import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False
}

def run_elt_script():
    script_path = "/opt/airflow/elt/elt_script.py"
    result = subprocess.run(["python", script_path],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed error duarr: {result.stderr}")
    else:
        print(result.stdout)

dag = DAG (
    'elt_and_dbt',
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2025, 3, 18),
    catchup=False
)

t1 = PythonOperator(
    task_id="run_elt_script",
    python_callable=run_elt_script,
    dag=dag
)

t2 = DockerOperator(
    task_id="dbt_run",
    image='ghcr.io/dbt-labs/dbt-postgres:1.9.0',
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/opt/dbt"
    ],
    auto_remove='success',
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
        Mount(source='/mnt/host/c/Work/2.Project-courses/elt-de/custom_postgres', target='/opt/dbt', type='bind'),
        Mount(source='/mnt/host/c/Users/812ha/.dbt', target='/root/.dbt', type='bind')
    ],
    dag=dag 
)

t1 >> t2