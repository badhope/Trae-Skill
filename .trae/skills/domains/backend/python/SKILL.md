---
name: backend-python
description: "Python backend development expert with FastAPI, Django, Flask, and async programming. Keywords: python, fastapi, django, flask, backend, api, rest"
layer: domain
role: specialist
version: 2.0.0
domain: backend
language: python
frameworks:
  - fastapi
  - django
  - flask
invoked_by:
  - coding-workflow
  - api-design
capabilities:
  - rest_api_development
  - async_programming
  - database_integration
  - authentication
  - testing
---

# Backend Python

Python后端开发专家，精通FastAPI、Django、Flask和异步编程。

## 适用场景

- 构建REST API
- 数据处理服务
- 机器学习后端
- Web应用程序
- 微服务架构

## 框架指南

### 1. FastAPI

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(
    title="User API",
    description="User management API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return user

@app.get("/users", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    return await UserService.get_all(skip, limit)

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await UserService.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    return await UserService.create(user)

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: UserBase):
    return await UserService.update(user_id, user)

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: str):
    await UserService.delete(user_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. Django

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
```

### 3. Flask

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, validate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class UserSchema(ma.Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    
    class Meta:
        fields = ('id', 'name', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@app.route('/users', methods=['POST'])
def create_user():
    data = user_schema.load(request.json)
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201
```

## 异步编程

```python
import asyncio
import aiohttp
from typing import List

async def fetch_multiple(urls: List[str]) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch_one(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()
```

## 最佳实践

1. **类型提示**: 使用type hints提高代码可读性
2. **虚拟环境**: 使用venv或poetry管理依赖
3. **环境变量**: 使用python-dotenv管理配置
4. **数据验证**: Pydantic进行数据验证
5. **测试**: pytest进行单元测试
6. **日志**: 结构化日志记录
7. **文档**: FastAPI自动生成API文档
8. **安全**: 遵循安全最佳实践

## 相关技能

- [api-design](../../actions/code/api-design) - API设计模式
- [data-pipeline](../../actions/analysis/data-pipeline) - 数据管道
- [backend-nodejs](../nodejs) - Node.js后端
- [backend-go](../go) - Go后端
