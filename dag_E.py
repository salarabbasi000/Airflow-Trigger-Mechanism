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
child_trigger = Dataset('file://trigger_E_update_F.txt')

with DAG(
    'dag_E',
    default_args=default_args,
    schedule=[parent_trigger],
    catchup=False,
    tags=['consuming']
) as dag:
    E1 = DummyOperator(task_id='E1')
    E2 = DummyOperator(task_id='E2')
    E3 = DummyOperator(task_id='E3')
    E4 = DummyOperator(task_id='E4')
    child_trigger_update = BashOperator(outlets=[child_trigger], task_id="producing_task_1", bash_command="sleep 3")

    E1 >> E2 >> E3 >> E4
