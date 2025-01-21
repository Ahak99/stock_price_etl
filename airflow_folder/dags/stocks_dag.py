# import os
# import sys

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
    
# python src/stock_price_etl/services/stocks_dag.py

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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import s3fs
import subprocess
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.services.data_extraction import data_extraction
from src.services.data_transformation import data_transformation

# Function to run unit tests
def run_tests():
    """
    Executes unit tests for the project and raises an exception if any test fails.
    """
    try:
        # Run all tests in the 'tests' directory
        result = subprocess.run(
            ["python", "-m", "unittest", "discover", "-s", "src/stock_price_etl/tests"],
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            raise Exception("Some tests failed. Check the logs for details.")
    except Exception as e:
        print(f"Test execution failed: {str(e)}")
        raise

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
test_task = PythonOperator(
    task_id='run_tests',
    python_callable=run_tests,
    dag=dag,
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
test_task >> extract_task >> transform_task
