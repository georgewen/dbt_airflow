from datetime import datetime

from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

SNOWFLAKE_CONN_ID = 'snowflake_conn'
SNOWFLAKE_SCHEMA = 'public'
SNOWFLAKE_WAREHOUSE = 'dbt_DEV_WH'
SNOWFLAKE_DATABASE = 'DEMO_DBT'
SNOWFLAKE_ROLE = 'dbt_DEV_ROLE'


dag = DAG(
    'example_snowflake',
    start_date=datetime(2021, 1, 1),
    default_args={'snowflake_conn_id': SNOWFLAKE_CONN_ID},
    tags=['example'],
    catchup=False,
)

COPY_TABLE_SQL_STRING = (
    f"copy into PUBLIC.BOOKINGS_1 from s3://gw-test-open-snowflake/airflow/ FILES=('bookings_1.csv') FILE_FORMAT=(TYPE='CSV' SKIP_HEADER=1);copy into PUBLIC.BOOKINGS_2 from s3://gw-test-open-snowflake/airflow/ FILES=('bookings_2.csv') FILE_FORMAT=(TYPE='CSV' SKIP_HEADER=1);"
)

snowflake_load = SnowflakeOperator(
    task_id='snowflake_copy_bookings',
    dag=dag,
    sql=COPY_TABLE_SQL_STRING,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    role=SNOWFLAKE_ROLE,
)

snowflake_load
