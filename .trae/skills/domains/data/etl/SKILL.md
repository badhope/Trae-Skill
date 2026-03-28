---
name: etl
description: "ETL pipeline development for data extraction, transformation, and loading. Keywords: etl, pipeline, data pipeline, airflow, spark, 数据管道"
layer: domain
role: specialist
version: 2.0.0
domain: data
languages:
  - python
  - sql
  - scala
frameworks:
  - apache-airflow
  - apache-spark
  - dbt
  - prefect
invoked_by:
  - coding-workflow
  - data-pipeline
capabilities:
  - data_extraction
  - data_transformation
  - data_loading
  - pipeline_orchestration
  - data_quality
---

# ETL Pipeline

ETL数据管道开发专家，专注于数据提取、转换和加载的完整流程。

## 适用场景

- 数据仓库构建
- 数据湖处理
- 实时数据流
- 批量数据处理
- 数据迁移

## 框架指南

### 1. Apache Airflow

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import pandas as pd
import json

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['data-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'user_analytics_pipeline',
    default_args=default_args,
    description='ETL pipeline for user analytics',
    schedule_interval='0 2 * * *',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['etl', 'analytics', 'users'],
) as dag:
    
    def extract_user_data(**context):
        postgres_hook = PostgresHook(postgres_conn_id='postgres_prod')
        records = postgres_hook.get_records("""
            SELECT 
                u.id,
                u.email,
                u.created_at,
                u.last_login,
                COUNT(o.id) as order_count,
                SUM(o.total) as total_spent
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            WHERE u.updated_at > '{{ ds }}'
            GROUP BY u.id
        """)
        
        df = pd.DataFrame(records, columns=[
            'id', 'email', 'created_at', 'last_login', 
            'order_count', 'total_spent'
        ])
        
        df.to_csv('/tmp/user_data.csv', index=False)
        return len(df)
    
    def transform_user_data(**context):
        df = pd.read_csv('/tmp/user_data.csv')
        
        df['total_spent'] = df['total_spent'].fillna(0)
        df['order_count'] = df['order_count'].fillna(0)
        
        df['user_segment'] = pd.cut(
            df['total_spent'],
            bins=[0, 100, 500, 1000, float('inf')],
            labels=['bronze', 'silver', 'gold', 'platinum']
        )
        
        df['days_since_last_login'] = (
            pd.Timestamp.now() - pd.to_datetime(df['last_login'])
        ).dt.days
        
        df['is_active'] = df['days_since_last_login'] <= 30
        
        df.to_csv('/tmp/user_data_transformed.csv', index=False)
        return len(df)
    
    def load_to_warehouse(**context):
        postgres_hook = PostgresHook(postgres_conn_id='postgres_warehouse')
        
        postgres_hook.run("""
            CREATE TABLE IF NOT EXISTS user_analytics (
                id VARCHAR(50) PRIMARY KEY,
                email VARCHAR(255),
                created_at TIMESTAMP,
                last_login TIMESTAMP,
                order_count INTEGER,
                total_spent DECIMAL(10, 2),
                user_segment VARCHAR(20),
                days_since_last_login INTEGER,
                is_active BOOLEAN,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        df = pd.read_csv('/tmp/user_data_transformed.csv')
        
        rows = []
        for _, row in df.iterrows():
            rows.append((
                row['id'],
                row['email'],
                row['created_at'],
                row['last_login'],
                int(row['order_count']),
                float(row['total_spent']),
                row['user_segment'],
                int(row['days_since_last_login']),
                bool(row['is_active'])
            ))
        
        postgres_hook.insert_rows(
            'user_analytics',
            rows,
            replace=True,
            replace_index=['id']
        )
        
        return len(rows)
    
    def upload_to_s3(**context):
        s3_hook = S3Hook(aws_conn_id='aws_default')
        
        s3_hook.load_file(
            filename='/tmp/user_data_transformed.csv',
            key=f'analytics/users/{{{{ ds }}}}/user_data.csv',
            bucket_name='data-lake',
            replace=True
        )
        
        return 's3://data-lake/analytics/users/{{ ds }}/user_data.csv'
    
    extract_task = PythonOperator(
        task_id='extract_user_data',
        python_callable=extract_user_data,
    )
    
    transform_task = PythonOperator(
        task_id='transform_user_data',
        python_callable=transform_user_data,
    )
    
    load_task = PythonOperator(
        task_id='load_to_warehouse',
        python_callable=load_to_warehouse,
    )
    
    s3_task = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
    )
    
    extract_task >> transform_task >> [load_task, s3_task]
```

### 2. Apache Spark

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, count, sum, avg, max, min,
    to_date, datediff, current_date, lit
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql.window import Window

class ETLPipeline:
    def __init__(self, app_name: str):
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .getOrCreate()
    
    def extract_from_database(self, jdbc_url: str, table: str, properties: dict):
        return self.spark.read \
            .jdbc(url=jdbc_url, table=table, properties=properties)
    
    def extract_from_s3(self, path: str, format: str = 'parquet'):
        if format == 'parquet':
            return self.spark.read.parquet(path)
        elif format == 'csv':
            return self.spark.read.csv(path, header=True, inferSchema=True)
        elif format == 'json':
            return self.spark.read.json(path)
    
    def transform_user_data(self, df):
        df = df.filter(col('email').isNotNull())
        
        df = df.withColumn(
            'user_segment',
            when(col('total_spent') >= 1000, 'platinum')
            .when(col('total_spent') >= 500, 'gold')
            .when(col('total_spent') >= 100, 'silver')
            .otherwise('bronze')
        )
        
        df = df.withColumn(
            'days_since_last_login',
            datediff(current_date(), col('last_login'))
        )
        
        df = df.withColumn(
            'is_active',
            when(col('days_since_last_login') <= 30, True).otherwise(False)
        )
        
        return df
    
    def transform_orders(self, orders_df, users_df):
        user_metrics = orders_df.groupBy('user_id').agg(
            count('id').alias('order_count'),
            sum('total').alias('total_spent'),
            avg('total').alias('avg_order_value'),
            max('created_at').alias('last_order_date')
        )
        
        return users_df.join(user_metrics, on='id', how='left')
    
    def transform_with_window(self, df):
        window_spec = Window.partitionBy('user_segment').orderBy(col('total_spent').desc())
        
        df = df.withColumn('rank_in_segment', row_number().over(window_spec))
        df = df.withColumn('percentile_in_segment', percent_rank().over(window_spec))
        
        return df
    
    def load_to_database(self, df, jdbc_url: str, table: str, properties: dict):
        df.write \
            .mode('overwrite') \
            .jdbc(url=jdbc_url, table=table, properties=properties)
    
    def load_to_s3(self, df, path: str, format: str = 'parquet', partition_by: list = None):
        writer = df.write.mode('overwrite')
        
        if partition_by:
            writer = writer.partitionBy(*partition_by)
        
        if format == 'parquet':
            writer.parquet(path)
        elif format == 'delta':
            writer.format('delta').save(path)
    
    def load_to_iceberg(self, df, table: str):
        df.writeTo(table).overwritePartitions()

def run_pipeline():
    etl = ETLPipeline('UserAnalyticsPipeline')
    
    users_df = etl.extract_from_s3('s3://data-lake/raw/users/', 'parquet')
    orders_df = etl.extract_from_s3('s3://data-lake/raw/orders/', 'parquet')
    
    users_with_metrics = etl.transform_orders(orders_df, users_df)
    transformed_df = etl.transform_user_data(users_with_metrics)
    
    etl.load_to_s3(
        transformed_df, 
        's3://data-lake/processed/user_analytics/',
        format='parquet',
        partition_by=['user_segment']
    )
    
    etl.load_to_iceberg(transformed_df, 'warehouse.user_analytics')

if __name__ == '__main__':
    run_pipeline()
```

### 3. dbt (Data Build Tool)

```sql
-- models/staging/stg_users.sql
with source as (
    select * from {{ source('raw', 'users') }}
),

cleaned as (
    select
        id as user_id,
        lower(trim(email)) as email,
        created_at,
        last_login,
        coalesce(updated_at, created_at) as updated_at
    from source
    where email is not null
)

select * from cleaned

-- models/staging/stg_orders.sql
with source as (
    select * from {{ source('raw', 'orders') }}
),

cleaned as (
    select
        id as order_id,
        user_id,
        total as order_total,
        status as order_status,
        created_at as order_created_at
    from source
    where total > 0
)

select * from cleaned

-- models/marts/user_analytics.sql
with users as (
    select * from {{ ref('stg_users') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

user_metrics as (
    select
        user_id,
        count(order_id) as order_count,
        sum(order_total) as total_spent,
        avg(order_total) as avg_order_value,
        max(order_created_at) as last_order_date
    from orders
    group by user_id
),

final as (
    select
        u.user_id,
        u.email,
        u.created_at,
        u.last_login,
        coalesce(um.order_count, 0) as order_count,
        coalesce(um.total_spent, 0) as total_spent,
        coalesce(um.avg_order_value, 0) as avg_order_value,
        um.last_order_date,
        case
            when coalesce(um.total_spent, 0) >= 1000 then 'platinum'
            when coalesce(um.total_spent, 0) >= 500 then 'gold'
            when coalesce(um.total_spent, 0) >= 100 then 'silver'
            else 'bronze'
        end as user_segment,
        datediff(day, u.last_login, current_date) as days_since_last_login,
        datediff(day, u.last_login, current_date) <= 30 as is_active
    from users u
    left join user_metrics um on u.user_id = um.user_id
)

select * from final
```

```yaml
# models/marts/schema.yml
version: 2

models:
  - name: user_analytics
    description: "User analytics with aggregated metrics"
    columns:
      - name: user_id
        description: "Unique user identifier"
        tests:
          - unique
          - not_null
      - name: email
        description: "User email address"
        tests:
          - unique
          - not_null
      - name: user_segment
        description: "User segment based on spending"
        tests:
          - accepted_values:
              values: ['bronze', 'silver', 'gold', 'platinum']
      - name: total_spent
        description: "Total amount spent by user"
        tests:
          - not_null
```

### 4. Prefect

```python
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import pandas as pd
import sqlalchemy

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def extract_data(query: str, connection_string: str) -> pd.DataFrame:
    engine = sqlalchemy.create_engine(connection_string)
    return pd.read_sql(query, engine)

@task
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df['total_spent'] = df['total_spent'].fillna(0)
    
    df['user_segment'] = pd.cut(
        df['total_spent'],
        bins=[0, 100, 500, 1000, float('inf')],
        labels=['bronze', 'silver', 'gold', 'platinum']
    )
    
    return df

@task
def load_data(df: pd.DataFrame, table: str, connection_string: str):
    engine = sqlalchemy.create_engine(connection_string)
    df.to_sql(table, engine, if_exists='replace', index=False)
    return len(df)

@flow(name="User Analytics ETL")
def user_analytics_etl(
    source_connection: str,
    target_connection: str,
    date: str = None
):
    query = f"""
        SELECT * FROM users
        WHERE updated_at >= '{date or '1900-01-01'}'
    """
    
    df = extract_data(query, source_connection)
    
    transformed_df = transform_data(df)
    
    rows_loaded = load_data(transformed_df, 'user_analytics', target_connection)
    
    return {"rows_loaded": rows_loaded}

if __name__ == "__main__":
    user_analytics_etl(
        source_connection="postgresql://user:pass@source:5432/db",
        target_connection="postgresql://user:pass@target:5432/warehouse"
    )
```

## 最佳实践

1. **幂等性**: ETL作业可重复执行
2. **增量处理**: 只处理变化数据
3. **数据质量**: 验证和清洗数据
4. **监控告警**: 任务失败通知
5. **文档化**: 数据血缘和转换逻辑
6. **测试**: 单元测试和集成测试
7. **版本控制**: 代码和配置版本化

## 相关技能

- [sql-optimization](../database/sql-optimization) - SQL优化
- [data-validation](../data-validation) - 数据验证
- [redis-caching](../database/redis-caching) - 缓存策略
- [backend-python](../backend/python) - Python后端
