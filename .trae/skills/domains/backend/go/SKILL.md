---
name: go
description: "Go language development for backend services, microservices, and cloud-native applications. Keywords: go, golang, gin, echo, fiber, go开发"
layer: domain
role: specialist
version: 2.0.0
domain: backend
language: go
frameworks:
  - gin
  - echo
  - fiber
invoked_by:
  - coding-workflow
  - code-generator
capabilities:
  - backend_development
  - microservices
  - concurrency
  - cloud_native
triggers:
  keywords:
    - go
    - golang
    - gin
    - echo
    - fiber
    - goroutine
    - channel
metrics:
  avg_execution_time: 3s
  success_rate: 0.95
  code_quality: 0.92
---

# Go Development

Go语言开发，用于后端服务、微服务和云原生应用。

## 目的

提供Go语言开发的最佳实践：
- 后端服务开发
- 微服务架构
- 并发编程
- 云原生应用

## 能力

- **后端开发**: Go后端服务开发
- **微服务**: 微服务架构设计
- **并发编程**: Goroutine和Channel
- **云原生**: 云原生应用开发

## 框架对比

| 框架 | 特点 | 适用场景 |
|------|------|----------|
| Gin | 高性能HTTP框架 | REST API |
| Echo | 简洁可扩展 | 微服务 |
| Fiber | Express风格 | 快速开发 |
| Chi | 轻量级路由 | 中间件链 |

## 项目结构

```
myapp/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── handler/
│   ├── service/
│   ├── repository/
│   └── model/
├── pkg/
│   └── utils/
├── api/
│   └── openapi.yaml
├── configs/
├── go.mod
└── go.sum
```

## Gin示例

```go
package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
)

type User struct {
    ID   string `json:"id"`
    Name string `json:"name"`
}

func main() {
    r := gin.Default()
    
    r.GET("/users/:id", getUser)
    r.POST("/users", createUser)
    
    r.Run(":8080")
}

func getUser(c *gin.Context) {
    id := c.Param("id")
    c.JSON(http.StatusOK, User{ID: id, Name: "John"})
}

func createUser(c *gin.Context) {
    var user User
    if err := c.ShouldBindJSON(&user); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    c.JSON(http.StatusCreated, user)
}
```

## 并发模式

### Goroutine

```go
func processData(data []int, results chan<- int) {
    for _, v := range data {
        results <- v * 2
    }
}

func main() {
    data := []int{1, 2, 3, 4, 5}
    results := make(chan int, len(data))
    
    go processData(data, results)
    
    for i := 0; i < len(data); i++ {
        fmt.Println(<-results)
    }
}
```

### Worker Pool

```go
func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        results <- j * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)
    
    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }
    
    for j := 1; j <= 5; j++ {
        jobs <- j
    }
    close(jobs)
    
    for r := 1; r <= 5; r++ {
        fmt.Println(<-results)
    }
}
```

## 错误处理

```go
type AppError struct {
    Code    int
    Message string
}

func (e *AppError) Error() string {
    return e.Message
}

func handleError(c *gin.Context, err error) {
    if appErr, ok := err.(*AppError); ok {
        c.JSON(appErr.Code, gin.H{"error": appErr.Message})
        return
    }
    c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal error"})
}
```

## 最佳实践

1. **项目结构**: 遵循标准Go项目布局
2. **错误处理**: 显式处理错误
3. **依赖管理**: 使用Go Modules
4. **并发安全**: 使用sync包保护共享资源
5. **测试**: 编写表驱动测试

## 相关技能

- [python](../python) - Python开发
- [nodejs](../nodejs) - Node.js开发
- [docker](../../devops/docker) - Docker容器
- [kubernetes](../../devops/kubernetes) - K8s编排
