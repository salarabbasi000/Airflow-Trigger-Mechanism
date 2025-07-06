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

parent_trigger = Dataset('file://trigger_B_update_D_E.txt')
child_trigger = Dataset('file://trigger_D_update_F.txt')

with DAG(
    'dag_D',
    default_args=default_args,
    schedule=[parent_trigger],
    catchup=False,
    tags=['consuming']
) as dag:
    D1 = DummyOperator(task_id='D1')
    D2 = DummyOperator(task_id='D2')
    child_trigger_update = BashOperator(outlets=[child_trigger], task_id="producing_task_1", bash_command="sleep 3")
    D3 = DummyOperator(task_id='D3')
    D4 = DummyOperator(task_id='D4')

    D1 >> D2 >> child_trigger_update >> D3 >> D4
