---
name: backend-nodejs
description: "Node.js backend development expert with Express, Fastify, NestJS, and TypeScript. Keywords: nodejs, express, nestjs, typescript, backend, api, rest"
layer: domain
role: specialist
version: 2.0.0
domain: backend
language: typescript
frameworks:
  - express
  - fastify
  - nestjs
invoked_by:
  - coding-workflow
  - api-design
capabilities:
  - rest_api_development
  - middleware_design
  - database_integration
  - authentication
  - testing
---

# Backend Node.js

Node.js后端开发专家，精通Express、Fastify、NestJS和TypeScript。

## 适用场景

- 构建REST API
- 创建微服务
- 实时应用程序
- 服务端应用
- API网关

## 框架指南

### 1. Express.js

```typescript
import express, { Request, Response, NextFunction, Router } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));

app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal Server Error' });
});

const userRouter = Router();

userRouter.get('/', async (req: Request, res: Response) => {
    const users = await UserService.findAll();
    res.json(users);
});

userRouter.post('/', async (req: Request, res: Response) => {
    const user = await UserService.create(req.body);
    res.status(201).json(user);
});

app.use('/api/users', userRouter);

app.listen(3000, () => console.log('Server running on port 3000'));
```

### 2. NestJS

```typescript
import { Controller, Get, Post, Body, Param, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';

@ApiTags('users')
@Controller('users')
export class UserController {
    constructor(private readonly userService: UserService) {}
    
    @Get()
    @ApiOperation({ summary: 'Get all users' })
    async findAll(): Promise<User[]> {
        return this.userService.findAll();
    }
    
    @Post()
    async create(@Body() createUserDto: CreateUserDto): Promise<User> {
        return this.userService.create(createUserDto);
    }
}
```

### 3. Fastify

```typescript
import Fastify from 'fastify';

const fastify = Fastify({ logger: true });

const userSchema = {
    type: 'object',
    required: ['name', 'email'],
    properties: {
        name: { type: 'string' },
        email: { type: 'string', format: 'email' }
    }
};

fastify.post('/users', {
    schema: { body: userSchema }
}, async (request, reply) => {
    const user = await UserService.create(request.body);
    reply.code(201).send(user);
});
```

## 中间件模式

```typescript
import jwt from 'jsonwebtoken';
import { z } from 'zod';

export const authMiddleware = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'No token' });
    
    try {
        req.user = jwt.verify(token, process.env.JWT_SECRET);
        next();
    } catch {
        res.status(401).json({ error: 'Invalid token' });
    }
};

export const validate = (schema: z.Schema) => (req, res, next) => {
    try {
        schema.parse(req.body);
        next();
    } catch (error) {
        res.status(400).json({ error: error.errors });
    }
};
```

## 数据库集成

```typescript
// Prisma
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function getUsers() {
    return prisma.user.findMany({ include: { posts: true } });
}

// TypeORM
@Entity('users')
export class User {
    @PrimaryGeneratedColumn('uuid')
    id: string;
    
    @Column()
    name: string;
    
    @Column({ unique: true })
    email: string;
}
```

## 最佳实践

1. **使用TypeScript**: 类型安全提高可维护性
2. **错误处理**: 集中式错误处理
3. **验证**: 使用Zod/Joi进行输入验证
4. **安全**: Helmet、CORS、限流
5. **日志**: 结构化日志(Winston、Pino)
6. **测试**: Jest单元/集成测试
7. **文档**: Swagger/OpenAPI
8. **环境**: 使用dotenv管理配置

## 相关技能

- [api-design](../../actions/code/api-design) - API设计模式
- [backend-python](../python) - Python后端
- [backend-go](../go) - Go后端
