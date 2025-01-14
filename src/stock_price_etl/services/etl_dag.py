# import os
# import sys
# import time

# # Add parent directory to the system path to access utils.py
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from datetime import timedelta
# from services.data_extraction import data_extraction
# from services.data_transformation import data_transformation

  
# def pipeline():
    
#     # print(f"\n#####   Start Data Transformation | Sector :  {sector}  ######\n")
#     print("* ******** * ********* * ******** *     Extraction begin     * ******** * ********* * ******** *")
#     data_extraction()
#     print("* ******** * ********* * ******** *     Transformation begin     * ******** * ********* * ******** *")
#     data_transformation()
#     # print(f"\n#####   End of Data Transformation | Sector :  {sector}  ######\n")

# if __name__ == "__main__":
#     pipeline()
    
# python src/data_pipeline/services/pipeline.py

# from datetime import timedelta
# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from airflow.utils.dates import days_ago
# from datetime import datetime
# from twitter_etl import run_twitter_etl

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2020, 11, 8),
#     'email': ['airflow@example.com'],
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=1)
# }

# dag = DAG(
#     'twitter_dag',
#     default_args=default_args,
#     description='Our first DAG with ETL process!',
#     schedule_interval=timedelta(days=1),
# )

# run_etl = PythonOperator(
#     task_id='complete_twitter_etl',
#     python_callable=run_twitter_etl,
#     dag=dag,
# )

# run_etl

import os
import sys
# Add parent directory to the system path to access utils.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from services.data_extraction import data_extraction
from services.data_transformation import data_transformation

def execute_extraction():
    print("""************************************************************************************************
             * ******** * ********* * ******** *     Extraction begin     * ******** * ********* * ******** *
             ************************************************************************************************""")
    data_extraction()

def execute_transformation():
    print("""****************************************************************************************************
             * ******** * ********* * ******** *     Transformation begin     * ******** * ********* * ******** *
             ****************************************************************************************************""")
    data_transformation()

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

# Instantiate the DAG
dag = DAG(
    'stock_price_dag',
    default_args=default_args,
    description='A DAG to perform data extraction and transformation',
    schedule_interval=timedelta(days=1),  # Set as needed (e.g., '@daily')
    start_date=datetime(2024, 9, 12),
    catchup=False,
)

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=execute_extraction,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=execute_transformation,
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task
