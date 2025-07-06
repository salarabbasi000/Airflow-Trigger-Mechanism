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

child_trigger = [Dataset('file://trigger_C_update_F.txt'), 
                 Dataset('file://trigger_D_update_F.txt'), 
                 Dataset('file://trigger_E_update_F.txt'),
                ]

with DAG(
    'dag_F',
    default_args=default_args,
    schedule=child_trigger,
    catchup=False,
    tags=['consuming']
) as dag:
    F1 = DummyOperator(task_id='F1')
    F2 = DummyOperator(task_id='F2')
    F3 = DummyOperator(task_id='F3')
    F4 = DummyOperator(task_id='F4')

    F1 >> F2 >> F3 >> F4