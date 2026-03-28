---
name: integration-test
description: "Integration testing for component interactions and API endpoints. Supports Supertest, pytest, TestContainers. Keywords: integration test, api test, 组件测试, 集成测试"
layer: domain
role: specialist
version: 2.0.0
domain: testing
languages:
  - javascript
  - typescript
  - python
  - go
  - java
frameworks:
  - supertest
  - pytest
  - testcontainers
  - spring-boot-test
invoked_by:
  - coding-workflow
  - test-generator
capabilities:
  - api_testing
  - database_testing
  - service_integration
  - contract_testing
  - test_fixtures
---

# Integration Test

集成测试专家，专注于组件间交互、API端点和数据库集成的测试。

## 适用场景

- API端点测试
- 数据库集成测试
- 服务间通信测试
- 第三方服务集成
- 契约测试

## 框架指南

### 1. Supertest + Jest (Node.js)

```javascript
const request = require('supertest');
const mongoose = require('mongoose');
const { app } = require('../app');
const User = require('../models/User');

describe('User API Integration Tests', () => {
  let server;
  
  beforeAll(async () => {
    const mongoUri = process.env.MONGODB_TEST_URI || 'mongodb://localhost:27017/test';
    await mongoose.connect(mongoUri);
    server = app.listen(0);
  });
  
  afterAll(async () => {
    await mongoose.connection.dropDatabase();
    await mongoose.connection.close();
    await server.close();
  });
  
  beforeEach(async () => {
    await User.deleteMany({});
  });
  
  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'SecurePass123!'
      };
      
      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect('Content-Type', /json/)
        .expect(201);
      
      expect(response.body.data).toMatchObject({
        name: userData.name,
        email: userData.email
      });
      expect(response.body.data.password).toBeUndefined();
      
      const dbUser = await User.findById(response.body.data.id);
      expect(dbUser).not.toBeNull();
    });
    
    it('should return 409 for duplicate email', async () => {
      await User.create({
        name: 'Existing',
        email: 'existing@example.com',
        password: 'hashedPassword'
      });
      
      const response = await request(app)
        .post('/api/users')
        .send({
          name: 'New User',
          email: 'existing@example.com',
          password: 'SecurePass123!'
        })
        .expect(409);
      
      expect(response.body.error).toContain('already exists');
    });
  });
  
  describe('GET /api/users/:id', () => {
    it('should return user by id', async () => {
      const user = await User.create({
        name: 'John',
        email: 'john@example.com',
        password: 'hashed'
      });
      
      const response = await request(app)
        .get(`/api/users/${user._id}`)
        .expect(200);
      
      expect(response.body.data.name).toBe('John');
    });
  });
  
  describe('Authentication Flow', () => {
    it('should authenticate user and access protected route', async () => {
      const userData = {
        name: 'Test User',
        email: 'test@example.com',
        password: 'SecurePass123!'
      };
      
      await request(app)
        .post('/api/users/register')
        .send(userData)
        .expect(201);
      
      const loginResponse = await request(app)
        .post('/api/auth/login')
        .send({
          email: userData.email,
          password: userData.password
        })
        .expect(200);
      
      const token = loginResponse.body.token;
      
      await request(app)
        .get('/api/users/me')
        .set('Authorization', `Bearer ${token}`)
        .expect(200);
    });
  });
});

describe('Database Integration', () => {
  describe('User Model', () => {
    it('should create user with hashed password', async () => {
      const user = await User.create({
        name: 'John',
        email: 'john@example.com',
        password: 'plainPassword'
      });
      
      expect(user.password).not.toBe('plainPassword');
      expect(await user.comparePassword('plainPassword')).toBe(true);
    });
    
    it('should enforce unique email', async () => {
      await User.create({
        name: 'User1',
        email: 'same@example.com',
        password: 'pass'
      });
      
      await expect(User.create({
        name: 'User2',
        email: 'same@example.com',
        password: 'pass'
      })).rejects.toThrow();
    });
  });
});
```

### 2. pytest + TestContainers (Python)

```python
import pytest
import asyncio
from httpx import AsyncClient
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from main import app, get_db, get_redis

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:7") as redis:
        yield redis

@pytest.fixture(scope="function")
def db_session(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Session = sessionmaker(bind=engine)
    
    from models import Base
    Base.metadata.create_all(engine)
    
    session = Session()
    yield session
    session.close()
    
    Base.metadata.drop_all(engine)

@pytest.fixture
def client(db_session, redis_container):
    def override_get_db():
        return db_session
    
    def override_get_redis():
        import redis
        return redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379)
        )
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

class TestUserAPI:
    """User API integration tests"""
    
    def test_create_user(self, client):
        response = client.post("/api/users", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123!"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert "password" not in data
    
    def test_create_duplicate_user(self, client):
        user_data = {
            "name": "John",
            "email": "john@example.com",
            "password": "SecurePass123!"
        }
        
        client.post("/api/users", json=user_data)
        
        response = client.post("/api/users", json=user_data)
        assert response.status_code == 409
    
    def test_get_user(self, client):
        create_response = client.post("/api/users", json={
            "name": "John",
            "email": "john@example.com",
            "password": "SecurePass123!"
        })
        user_id = create_response.json()["id"]
        
        response = client.get(f"/api/users/{user_id}")
        
        assert response.status_code == 200
        assert response.json()["name"] == "John"
    
    def test_auth_flow(self, client):
        client.post("/api/auth/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "SecurePass123!"
        })
        
        login_response = client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        })
        
        assert login_response.status_code == 200
        token = login_response.json()["token"]
        
        me_response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "test@example.com"

class TestCacheIntegration:
    """Redis cache integration tests"""
    
    def test_cache_hit(self, client, redis_container):
        import redis
        r = redis.Redis(
            host=redis_container.get_container_host_ip(),
            port=redis_container.get_exposed_port(6379)
        )
        
        r.set("user:1", '{"name": "Cached User"}')
        
        response = client.get("/api/users/1")
        
        assert response.status_code == 200
        assert response.json()["name"] == "Cached User"

@pytest.mark.asyncio
async def test_async_api():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/users", json={
            "name": "Async User",
            "email": "async@example.com",
            "password": "SecurePass123!"
        })
        
        assert response.status_code == 201
```

### 3. Spring Boot Test (Java)

```java
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import com.fasterxml.jackson.databind.ObjectMapper;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.hamcrest.Matchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
class UserApiIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15");
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
    
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Autowired
    private UserRepository userRepository;
    
    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }
    
    @Test
    void shouldCreateUser() throws Exception {
        String userJson = objectMapper.writeValueAsString(Map.of(
            "name", "John Doe",
            "email", "john@example.com",
            "password", "SecurePass123!"
        ));
        
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(userJson))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.name").value("John Doe"))
            .andExpect(jsonPath("$.email").value("john@example.com"))
            .andExpect(jsonPath("$.password").doesNotExist());
    }
    
    @Test
    void shouldReturnConflictForDuplicateEmail() throws Exception {
        userRepository.save(new User("Existing", "existing@example.com", "hashed"));
        
        String userJson = objectMapper.writeValueAsString(Map.of(
            "name", "New User",
            "email", "existing@example.com",
            "password", "SecurePass123!"
        ));
        
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(userJson))
            .andExpect(status().isConflict());
    }
    
    @Test
    void shouldAuthenticateAndAccessProtectedRoute() throws Exception {
        String registerJson = objectMapper.writeValueAsString(Map.of(
            "name", "Test User",
            "email", "test@example.com",
            "password", "SecurePass123!"
        ));
        
        mockMvc.perform(post("/api/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(registerJson))
            .andExpect(status().isCreated());
        
        String loginJson = objectMapper.writeValueAsString(Map.of(
            "email", "test@example.com",
            "password", "SecurePass123!"
        ));
        
        String response = mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(loginJson))
            .andExpect(status().isOk())
            .andReturn().getResponse().getContentAsString();
        
        String token = objectMapper.readTree(response).get("token").asText();
        
        mockMvc.perform(get("/api/users/me")
                .header("Authorization", "Bearer " + token))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.email").value("test@example.com"));
    }
}
```

## 测试策略

### 测试金字塔

```
        /\
       /  \      E2E Tests (慢、昂贵)
      /----\     
     /      \    Integration Tests (中等)
    /--------\   
   /          \  Unit Tests (快、便宜)
  /------------\
```

### 数据库测试模式

```javascript
describe('Database Tests', () => {
  beforeEach(async () => {
    await sequelize.sync({ force: true });
  });
  
  afterEach(async () => {
    await sequelize.drop();
  });
  
  it('should handle transactions', async () => {
    const transaction = await sequelize.transaction();
    
    try {
      await User.create({ name: 'User1' }, { transaction });
      await Order.create({ userId: 1 }, { transaction });
      await transaction.commit();
    } catch (error) {
      await transaction.rollback();
      throw error;
    }
  });
});
```

## 最佳实践

1. **真实环境**: 使用真实数据库和依赖
2. **隔离测试**: 每个测试独立数据
3. **清理数据**: 测试前后清理状态
4. **使用容器**: TestContainers提供一致性
5. **契约测试**: 验证服务间接口
6. **性能基准**: 监控测试执行时间

## 相关技能

- [unit-test](../unit-test) - 单元测试
- [e2e-test](../e2e-test) - 端到端测试
- [api-design](../../actions/code/api-design) - API设计
- [database-migration](../database/database-migration) - 数据库迁移
