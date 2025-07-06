from airflow import DAG, Dataset
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'email': ['salarabbasi000@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

child_trigger = Dataset('file://trigger_B_update_D_E.txt')

with DAG(
    'dag_B',
    default_args=default_args,
    schedule_interval='0 6 * * *',
    catchup=False,
    tags=['consuming']
) as dag:
    B1 = DummyOperator(task_id='B1')
    B2 = DummyOperator(task_id='B2')
    B3 = DummyOperator(task_id='B3')
    child_trigger_update = BashOperator(outlets=[child_trigger], task_id="producing_task_1", bash_command="sleep 3")
    B4 = DummyOperator(task_id='B4')

    B1 >> B2 >> B3 >> child_trigger_update >> B4
