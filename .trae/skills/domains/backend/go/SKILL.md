---
name: backend-go
description: "Go backend development expert with Gin, Echo, gRPC, and concurrent programming. Keywords: go, golang, gin, grpc, backend, api, microservices"
layer: domain
role: specialist
version: 2.0.0
domain: backend
language: go
frameworks:
  - gin
  - echo
  - grpc
invoked_by:
  - coding-workflow
  - api-design
capabilities:
  - high_performance_api
  - concurrent_programming
  - microservices
  - grpc_services
  - system_tools
---

# Backend Go

Go后端开发专家，精通Gin、Echo、gRPC和并发编程。

## 适用场景

- 高性能API
- 微服务架构
- 系统工具
- 实时应用
- 云原生服务

## 框架指南

### 1. Gin

```go
package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

type User struct {
    ID    uint   `json:"id"`
    Name  string `json:"name" binding:"required"`
    Email string `json:"email" binding:"required,email"`
}

func main() {
    r := gin.Default()
    
    r.Use(CORSMiddleware())
    r.Use(AuthMiddleware())
    
    users := r.Group("/api/users")
    {
        users.GET("", getUsers)
        users.POST("", createUser)
        users.GET("/:id", getUser)
        users.PUT("/:id", updateUser)
        users.DELETE("/:id", deleteUser)
    }
    
    r.Run(":8080")
}

func createUser(c *gin.Context) {
    var user User
    if err := c.ShouldBindJSON(&user); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    user.ID = nextID
    nextID++
    users[user.ID] = user
    c.JSON(http.StatusCreated, user)
}
```

### 2. gRPC

```protobuf
syntax = "proto3";
package user;

service UserService {
    rpc GetUser(GetUserRequest) returns (User);
    rpc CreateUser(CreateUserRequest) returns (User);
    rpc ListUsers(ListUsersRequest) returns (stream User);
}

message User {
    uint32 id = 1;
    string name = 2;
    string email = 3;
}
```

```go
func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    return &pb.User{Id: req.Id, Name: "John", Email: "john@example.com"}, nil
}
```

## 并发模式

```go
// Worker Pool
func workerPool(jobs <-chan Job, results chan<- Result, workers int) {
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }()
    }
    wg.Wait()
    close(results)
}

// Context with Timeout
func fetchWithTimeout(ctx context.Context, url string) (*http.Response, error) {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    return http.DefaultClient.Do(req)
}
```

## 数据库集成

```go
// GORM
import "gorm.io/gorm"

type User struct {
    gorm.Model
    Name  string
    Email string `gorm:"unique"`
}

func main() {
    db, _ := gorm.Open(postgres.Open(dsn), &gorm.Config{})
    db.AutoMigrate(&User{})
    db.Create(&User{Name: "John", Email: "john@example.com"})
}
```

## 最佳实践

1. **错误处理**: 显式处理错误
2. **Context**: 用于取消和超时
3. **并发**: 合理使用goroutine和channel
4. **测试**: 编写表驱动测试
5. **文档**: 文档化导出函数
6. **格式化**: 使用gofmt和goimports
7. **Lint**: 使用golangci-lint
8. **依赖**: 使用Go modules

## 相关技能

- [api-design](../../actions/code/api-design) - API设计模式
- [backend-python](../python) - Python后端
- [backend-nodejs](../nodejs) - Node.js后端
