---
name: rust
description: "Rust systems programming for safe, concurrent, and high-performance applications. Keywords: rust, cargo, tokio, actix, rust开发, 系统编程"
layer: domain
role: specialist
version: 2.0.0
domain: backend
language: rust
frameworks:
  - tokio
  - actix-web
  - axum
invoked_by:
  - coding-workflow
  - code-generator
capabilities:
  - systems_programming
  - concurrent_programming
  - memory_safety
  - web_services
triggers:
  keywords:
    - rust
    - cargo
    - tokio
    - actix
    - axum
    - rust开发
    - 系统编程
metrics:
  avg_execution_time: 4s
  success_rate: 0.93
  code_quality: 0.95
---

# Rust Development

Rust系统编程，用于安全、并发和高性能应用开发。

## 目的

提供Rust开发的最佳实践：
- 系统级编程
- 并发编程
- 内存安全
- Web服务开发

## 能力

- **系统编程**: 底层系统开发
- **并发编程**: 异步和多线程
- **内存安全**: 无GC内存管理
- **Web服务**: 高性能后端服务

## 框架对比

| 框架 | 特点 | 适用场景 |
|------|------|----------|
| Actix-web | 功能完整 | 企业级应用 |
| Axum | 简洁现代 | Tokio生态 |
| Warp | 函数式 | API服务 |
| Rocket | 易用性 | 快速开发 |

## 项目结构

```
myapp/
├── Cargo.toml
├── Cargo.lock
├── src/
│   ├── main.rs
│   ├── lib.rs
│   ├── api/
│   │   ├── mod.rs
│   │   └── handlers.rs
│   ├── models/
│   │   └── mod.rs
│   └── utils/
│       └── mod.rs
├── tests/
│   └── integration_test.rs
└── benches/
    └── benchmark.rs
```

## Axum示例

```rust
use axum::{
    extract::Path,
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;

#[derive(Serialize, Deserialize)]
struct User {
    id: u64,
    name: String,
    email: String,
}

async fn get_user(Path(id): Path<u64>) -> Result<Json<User>, StatusCode> {
    let user = User {
        id,
        name: "John".to_string(),
        email: "john@example.com".to_string(),
    };
    Ok(Json(user))
}

async fn create_user(Json(user): Json<User>) -> Result<Json<User>, StatusCode> {
    Ok(Json(user))
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/users/:id", get(get_user))
        .route("/users", post(create_user));

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```

## 异步编程

### Tokio

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        sleep(Duration::from_secs(1)).await;
        42
    });

    let result = handle.await.unwrap();
    println!("Result: {}", result);
}
```

### 并发任务

```rust
use tokio::task::JoinSet;

async fn process_items(items: Vec<i32>) -> Vec<i32> {
    let mut set = JoinSet::new();

    for item in items {
        set.spawn(async move {
            item * 2
        });
    }

    let mut results = Vec::new();
    while let Some(res) = set.join_next().await {
        results.push(res.unwrap());
    }
    results
}
```

## 错误处理

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    
    #[error("Not found: {0}")]
    NotFound(String),
    
    #[error("Validation error: {0}")]
    Validation(String),
}

pub type Result<T> = std::result::Result<T, AppError>;
```

## 内存安全模式

### 所有权

```rust
fn take_ownership(s: String) {
    println!("{}", s);
}

fn borrow_value(s: &String) {
    println!("{}", s);
}

fn mutate_value(s: &mut String) {
    s.push_str(" modified");
}

fn main() {
    let s = String::from("hello");
    borrow_value(&s);
    println!("{}", s);

    let mut s2 = String::from("hello");
    mutate_value(&mut s2);
    println!("{}", s2);

    take_ownership(s);
}
```

### 生命周期

```rust
struct Parser<'a> {
    input: &'a str,
}

impl<'a> Parser<'a> {
    fn new(input: &'a str) -> Self {
        Parser { input }
    }

    fn parse(&self) -> &'a str {
        self.input
    }
}
```

## 测试

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_user_creation() {
        let user = User {
            id: 1,
            name: "Test".to_string(),
            email: "test@example.com".to_string(),
        };
        assert_eq!(user.id, 1);
    }

    #[tokio::test]
    async fn test_async_operation() {
        let result = async_function().await;
        assert!(result.is_ok());
    }
}
```

## 最佳实践

1. **错误处理**: 使用Result和thiserror
2. **异步**: 使用Tokio运行时
3. **测试**: 编写单元测试和集成测试
4. **文档**: 使用rustdoc注释
5. **格式化**: 使用rustfmt和clippy

## 相关技能

- [go](../go) - Go开发
- [python](../python) - Python开发
- [docker](../../devops/docker) - Docker容器
- [kubernetes](../../devops/kubernetes) - K8s编排
