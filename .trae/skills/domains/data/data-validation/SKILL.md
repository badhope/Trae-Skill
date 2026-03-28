---
name: data-validation
description: "Data validation and quality assurance for data pipelines. Keywords: validation, data quality, schema, pydantic, great-expectations, 数据验证"
layer: domain
role: specialist
version: 2.0.0
domain: data
languages:
  - python
  - sql
frameworks:
  - pydantic
  - great-expectations
  - pandera
  - cerberus
invoked_by:
  - coding-workflow
  - etl
capabilities:
  - schema_validation
  - data_quality_checks
  - anomaly_detection
  - data_profiling
  - validation_rules
---

# Data Validation

数据验证专家，确保数据质量和完整性，防止脏数据进入系统。

## 适用场景

- API输入验证
- ETL数据质量检查
- 数据库约束验证
- 配置文件验证
- 消息队列数据验证

## 框架指南

### 1. Pydantic

```python
from pydantic import BaseModel, Field, validator, root_validator, EmailStr, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum
import re

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class Address(BaseModel):
    street: str = Field(..., min_length=5, max_length=200)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')
    country: str = Field(..., min_length=2, max_length=2)

class User(BaseModel):
    id: str = Field(..., pattern=r'^usr_[a-zA-Z0-9]{16}$')
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    status: UserStatus = UserStatus.ACTIVE
    age: Optional[int] = Field(None, ge=0, le=150)
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    address: Optional[Address] = None
    tags: List[str] = Field(default_factory=list, max_items=10)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    @validator('name')
    def name_must_not_contain_numbers(cls, v):
        if re.search(r'\d', v):
            raise ValueError('Name must not contain numbers')
        return v.title()
    
    @validator('tags', each_item=True)
    def tag_must_be_lowercase(cls, v):
        if not v.islower():
            raise ValueError('Tags must be lowercase')
        return v
    
    @root_validator
    def check_age_and_status(cls, values):
        age = values.get('age')
        status = values.get('status')
        
        if age is not None and age < 18 and status == UserStatus.ACTIVE:
            raise ValueError('Users under 18 cannot be active')
        
        return values
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def password_strength(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain special character')
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    status: Optional[UserStatus] = None
    address: Optional[Address] = None

class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)

class Order(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem] = Field(..., min_items=1)
    total: float = Field(..., ge=0)
    status: str = "pending"
    
    @root_validator
    def validate_total(cls, values):
        items = values.get('items', [])
        total = values.get('total', 0)
        
        calculated_total = sum(
            item.quantity * item.unit_price 
            for item in items
        )
        
        if abs(calculated_total - total) > 0.01:
            raise ValueError(
                f'Total {total} does not match calculated {calculated_total}'
            )
        
        return values

def validate_api_response(data: dict, model: type) -> tuple[bool, Optional[str]]:
    try:
        model(**data)
        return True, None
    except ValueError as e:
        return False, str(e)

valid_user = User(
    id="usr_abc123def456ghi7",
    email="john@example.com",
    name="John Doe",
    age=30,
    tags=["premium", "verified"]
)

print(valid_user.json())
print(valid_user.dict())
```

### 2. Great Expectations

```python
import great_expectations as gx
from great_expectations.dataset import PandasDataset
import pandas as pd

context = gx.get_context()

df = pd.DataFrame({
    'user_id': ['usr_001', 'usr_002', 'usr_003'],
    'email': ['john@example.com', 'jane@example.com', 'bob@example.com'],
    'age': [25, 30, 35],
    'total_spent': [100.50, 250.00, 75.25],
    'created_at': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03'])
})

suite = context.add_expectation_suite("user_data_expectations")

validator = context.get_validator(
    batch_request={
        "datasource_name": "pandas_datasource",
        "data_asset_name": "user_data",
    },
    expectation_suite_name="user_data_expectations"
)

validator.expect_table_row_count_to_be_between(min_value=1, max_value=1000000)

validator.expect_column_to_exist("user_id")
validator.expect_column_to_exist("email")
validator.expect_column_to_exist("age")

validator.expect_column_values_to_not_be_null("user_id")
validator.expect_column_values_to_not_be_null("email")

validator.expect_column_values_to_be_unique("user_id")

validator.expect_column_values_to_match_regex(
    "user_id", 
    r"^usr_[a-zA-Z0-9]+$"
)

validator.expect_column_values_to_match_regex(
    "email",
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

validator.expect_column_values_to_be_between(
    "age",
    min_value=0,
    max_value=150
)

validator.expect_column_values_to_be_between(
    "total_spent",
    min_value=0,
    max_value=1000000
)

validator.expect_column_values_to_be_in_type_list(
    "age",
    ["integer", "int64", "int32"]
)

validator.expect_column_values_to_be_in_type_list(
    "total_spent",
    ["float", "float64", "float32"]
)

validator.save_expectation_suite()

checkpoint = context.add_or_update_checkpoint(
    name="user_data_checkpoint",
    validations=[
        {
            "batch_request": {
                "datasource_name": "pandas_datasource",
                "data_asset_name": "user_data",
            },
            "expectation_suite_name": "user_data_expectations"
        }
    ]
)

results = checkpoint.run()

if results.success:
    print("All validations passed!")
else:
    print("Validation failed!")
    for validation_result in results.run_results.values():
        for result in validation_result["validation_result"].results:
            if not result.success:
                print(f"Failed: {result.expectation_config.expectation_type}")
                print(f"Details: {result.result}")

suite = context.add_expectation_suite("order_data_expectations")

validator = context.get_validator(
    batch_request={
        "datasource_name": "pandas_datasource",
        "data_asset_name": "order_data",
    },
    expectation_suite_name="order_data_expectations"
)

validator.expect_column_values_to_be_between(
    "order_total",
    min_value=0,
    max_value=100000,
    mostly=0.99
)

validator.expect_compound_columns_to_be_unique(
    ["user_id", "order_date"]
)

validator.expect_column_pair_values_A_to_be_greater_than_B(
    column_A="total_with_tax",
    column_B="total_without_tax"
)

validator.expect_column_values_to_be_in_set(
    "status",
    value_set=["pending", "processing", "shipped", "delivered", "cancelled"]
)

validator.expect_column_values_to_match_strftime_format(
    "created_at",
    strftime_format="%Y-%m-%d %H:%M:%S"
)
```

### 3. Pandera

```python
import pandera as pa
from pandera import Column, DataFrameSchema, Check, Index
import pandas as pd
from typing import Optional

schema = DataFrameSchema(
    columns={
        "user_id": Column(
            str,
            checks=[
                Check.str_matches(r"^usr_[a-zA-Z0-9]+$"),
            ],
            nullable=False,
            unique=True
        ),
        "email": Column(
            str,
            checks=[
                Check.str_matches(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
            ],
            nullable=False
        ),
        "age": Column(
            int,
            checks=[
                Check.ge(0),
                Check.le(150),
            ],
            nullable=True
        ),
        "total_spent": Column(
            float,
            checks=[
                Check.ge(0),
                Check.lt(1000000),
            ],
            nullable=False
        ),
        "status": Column(
            str,
            checks=[
                Check.isin(["active", "inactive", "suspended"]),
            ],
            nullable=False
        ),
        "created_at": Column(
            "datetime64[ns]",
            nullable=False
        ),
    },
    index=Index(int, name="row_id"),
    strict=True,
    coerce=True
)

@pa.check_input(schema)
def process_users(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("status").agg({
        "total_spent": "mean",
        "age": "mean"
    })

df = pd.DataFrame({
    "user_id": ["usr_001", "usr_002", "usr_003"],
    "email": ["john@example.com", "jane@example.com", "bob@example.com"],
    "age": [25, 30, 35],
    "total_spent": [100.50, 250.00, 75.25],
    "status": ["active", "active", "inactive"],
    "created_at": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"])
})

validated_df = schema.validate(df)

class UserSchema(pa.SchemaModel):
    user_id: str = pa.Field(pattern=r"^usr_[a-zA-Z0-9]+$", unique=True)
    email: str = pa.Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    age: Optional[int] = pa.Field(ge=0, le=150, nullable=True)
    total_spent: float = pa.Field(ge=0)
    status: str = pa.Field(isin=["active", "inactive", "suspended"])
    
    @pa.check("age")
    @classmethod
    def age_must_be_reasonable(cls, series: pd.Series) -> pd.Series:
        return series.dropna().apply(lambda x: 0 <= x <= 150)
    
    class Config:
        strict = True
        coerce = True

@pa.check_types
def process_users_typed(df: DataFrame[UserSchema]) -> DataFrame[UserSchema]:
    return df
```

### 4. SQL数据验证

```sql
CREATE TABLE users (
    id VARCHAR(20) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    age INTEGER CHECK (age >= 0 AND age <= 150),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    total_spent DECIMAL(10, 2) DEFAULT 0 CHECK (total_spent >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT valid_status CHECK (status IN ('active', 'inactive', 'suspended')),
    CONSTRAINT valid_id_format CHECK (id ~ '^usr_[a-zA-Z0-9]+$')
);

CREATE OR REPLACE FUNCTION validate_user_data()
RETURNS TABLE(
    validation_type TEXT,
    failed_count INTEGER,
    sample_values TEXT[]
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'null_emails'::TEXT,
        COUNT(*)::INTEGER,
        ARRAY_AGG(email LIMIT 5)
    FROM users WHERE email IS NULL
    
    UNION ALL
    
    SELECT 
        'invalid_emails'::TEXT,
        COUNT(*)::INTEGER,
        ARRAY_AGG(email LIMIT 5)
    FROM users 
    WHERE email !~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    
    UNION ALL
    
    SELECT 
        'duplicate_emails'::TEXT,
        COUNT(*)::INTEGER,
        ARRAY_AGG(email LIMIT 5)
    FROM (
        SELECT email, COUNT(*) as cnt
        FROM users
        GROUP BY email
        HAVING COUNT(*) > 1
    ) dup
    
    UNION ALL
    
    SELECT 
        'invalid_age'::TEXT,
        COUNT(*)::INTEGER,
        ARRAY_AGG(age::TEXT LIMIT 5)
    FROM users 
    WHERE age IS NOT NULL AND (age < 0 OR age > 150)
    
    UNION ALL
    
    SELECT 
        'negative_spent'::TEXT,
        COUNT(*)::INTEGER,
        ARRAY_AGG(total_spent::TEXT LIMIT 5)
    FROM users 
    WHERE total_spent < 0;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM validate_user_data();
```

## 最佳实践

1. **尽早验证**: 在数据入口处验证
2. **明确错误**: 提供清晰的错误信息
3. **分层验证**: 格式、业务规则、跨字段验证
4. **可配置规则**: 验证规则可动态调整
5. **监控告警**: 验证失败及时通知
6. **数据血缘**: 追踪数据来源和转换

## 相关技能

- [etl](../etl) - ETL管道
- [sql-optimization](../database/sql-optimization) - SQL优化
- [backend-python](../backend/python) - Python后端
- [api-design](../../actions/code/api-design) - API设计
