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

child_trigger = Dataset('file://trigger_A_update_C.txt')

with DAG(
    'dag_A',
    default_args=default_args,
    schedule_interval='0 5 * * *',
    catchup=False,
    tags=['producing']
) as dag:
    A1 = DummyOperator(task_id='A1')
    A2 = DummyOperator(task_id='A2')
    A3 = DummyOperator(task_id='A3')
    child_trigger_update = BashOperator(outlets=[child_trigger], task_id="producing_task_1", bash_command="sleep 3")
    A4 = DummyOperator(task_id='A4')

    A1 >> A2 >> A3 >> child_trigger_update >> A4