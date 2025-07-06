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

parent_trigger = Dataset('file://trigger_A_update_C.txt')
child_trigger = Dataset('file://trigger_C_update_F.txt')

with DAG(
    'dag_C',
    default_args=default_args,
    schedule=[parent_trigger],
    catchup=False,
    tags=['consuming']
) as dag:
    C1 = DummyOperator(task_id='C1')
    child_trigger_update = BashOperator(outlets=[child_trigger], task_id="producing_task_1", bash_command="sleep 3")
    C2 = DummyOperator(task_id='C2')
    C3 = DummyOperator(task_id='C3')
    C4 = DummyOperator(task_id='C4')

    C1 >> child_trigger_update >> C2 >> C3 >> C4
