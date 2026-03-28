---
name: documentation
description: "Documentation generation and maintenance for code, APIs, and projects. Keywords: docs, documentation, readme, api-docs, swagger, 文档"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
  - api-design
capabilities:
  - readme_generation
  - api_documentation
  - code_comments
  - changelog_generation
  - architecture_docs
triggers:
  keywords:
    - document
    - docs
    - readme
    - documentation
    - 文档
metrics:
  avg_execution_time: 2s
  success_rate: 0.95
---

# Documentation

文档生成专家，为代码、API和项目生成高质量文档。

## 适用场景

- README文件生成
- API文档生成
- 代码注释添加
- CHANGELOG维护
- 架构文档编写

## 文档类型

### 1. README模板

```markdown
# Project Name

Brief description of what this project does and who it's for.

## Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Quick Start

### Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0

### Installation

```bash
npm install project-name
```

### Basic Usage

```javascript
import { Client } from 'project-name';

const client = new Client({
  apiKey: process.env.API_KEY
});

const result = await client.doSomething();
console.log(result);
```

## API Reference

### `Client`

Main client for interacting with the API.

#### Constructor

```javascript
new Client(options: ClientOptions)
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| apiKey | string | Yes | Your API key |
| baseUrl | string | No | Custom base URL |
| timeout | number | No | Request timeout in ms |

#### Methods

##### `doSomething()`

Performs an action.

```javascript
const result = await client.doSomething(options);
```

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | string | Yes | First parameter |
| param2 | number | No | Second parameter |

**Returns:** `Promise<Result>`

**Example:**

```javascript
const result = await client.doSomething({
  param1: 'value',
  param2: 42
});
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| API_KEY | Your API key | - |
| DEBUG | Enable debug mode | false |

## Examples

### Example 1: Basic Usage

```javascript
// example-basic.js
import { Client } from 'project-name';

const client = new Client({ apiKey: 'your-key' });
const result = await client.doSomething();
```

### Example 2: Advanced Usage

```javascript
// example-advanced.js
import { Client } from 'project-name';

const client = new Client({
  apiKey: process.env.API_KEY,
  baseUrl: 'https://custom.api.com',
  timeout: 30000
});
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
```

### 2. API文档 (OpenAPI/Swagger)

```yaml
openapi: 3.0.3
info:
  title: User API
  description: API for managing users
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

tags:
  - name: Users
    description: User management operations
  - name: Auth
    description: Authentication operations

paths:
  /users:
    get:
      tags:
        - Users
      summary: List all users
      description: Returns a paginated list of users
      operationId: listUsers
      parameters:
        - name: page
          in: query
          description: Page number
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          description: Items per page
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: status
          in: query
          description: Filter by status
          schema:
            type: string
            enum: [active, inactive, suspended]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/ServerError'
    
    post:
      tags:
        - Users
      summary: Create a new user
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: Email already exists

  /users/{userId}:
    get:
      tags:
        - Users
      summary: Get user by ID
      operationId: getUser
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            pattern: '^usr_[a-zA-Z0-9]+$'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          example: usr_abc123def456
        email:
          type: string
          format: email
          example: john@example.com
        name:
          type: string
          example: John Doe
        status:
          type: string
          enum: [active, inactive, suspended]
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
    
    UserCreate:
      type: object
      required:
        - email
        - name
        - password
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 2
          maxLength: 100
        password:
          type: string
          format: password
          minLength: 8
    
    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'
    
    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer
    
    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: object

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Unauthorized
    NotFound:
      description: Resource not found
    ServerError:
      description: Internal server error

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

### 3. 代码注释规范

```typescript
/**
 * Represents a user in the system.
 * 
 * @example
 * ```typescript
 * const user = new User({
 *   email: 'john@example.com',
 *   name: 'John Doe'
 * });
 * ```
 */
class User {
  /**
   * Unique identifier for the user.
   * Format: usr_[a-zA-Z0-9]+
   */
  public readonly id: string;
  
  /**
   * User's email address.
   * Must be a valid email format.
   */
  public email: string;
  
  /**
   * User's display name.
   * @minLength 2
   * @maxLength 100
   */
  public name: string;
  
  /**
   * Creates a new User instance.
   * 
   * @param data - The user data
   * @throws {ValidationError} If email format is invalid
   * 
   * @example
   * ```typescript
   * const user = new User({
   *   email: 'john@example.com',
   *   name: 'John Doe'
   * });
   * ```
   */
  constructor(data: UserData) {
    this.validate(data);
    this.id = generateId();
    this.email = data.email;
    this.name = data.name;
  }
  
  /**
   * Updates the user's profile.
   * 
   * @param updates - The fields to update
   * @returns The updated user
   * @throws {ValidationError} If updates are invalid
   * 
   * @example
   * ```typescript
   * user.update({ name: 'Jane Doe' });
   * ```
   */
  update(updates: Partial<UserData>): User {
    Object.assign(this, updates);
    return this;
  }
  
  /**
   * Validates user data.
   * 
   * @private
   * @param data - Data to validate
   * @throws {ValidationError} If validation fails
   */
  private validate(data: UserData): void {
    if (!isValidEmail(data.email)) {
      throw new ValidationError('Invalid email format');
    }
  }
}

/**
 * Configuration options for the API client.
 * 
 * @interface ClientOptions
 */
interface ClientOptions {
  /** API key for authentication */
  apiKey: string;
  
  /** Base URL for API requests */
  baseUrl?: string;
  
  /** Request timeout in milliseconds */
  timeout?: number;
  
  /** Enable debug logging */
  debug?: boolean;
}

/**
 * Result of an API operation.
 * 
 * @template T - The type of the result data
 */
interface Result<T> {
  /** Whether the operation was successful */
  success: boolean;
  
  /** The result data if successful */
  data?: T;
  
  /** Error message if failed */
  error?: string;
}
```

### 4. CHANGELOG模板

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

### Changed
- Change description

### Fixed
- Bug fix description

## [1.2.0] - 2025-03-15

### Added
- Feature: Add user profile endpoint (#123)
- Feature: Support pagination for user list (#125)

### Changed
- Improve API response time by 30%
- Update dependencies to latest versions

### Fixed
- Fix memory leak in connection pool (#127)
- Fix incorrect timestamp format in responses (#128)

### Security
- Update JWT library to fix CVE-2025-1234

## [1.1.0] - 2025-02-01

### Added
- Feature: Add bulk import functionality
- Feature: Add webhook support

### Changed
- Deprecate old API endpoints (will be removed in v2.0)

### Fixed
- Fix race condition in async operations

## [1.0.0] - 2025-01-01

### Added
- Initial release
- User management API
- Authentication with JWT
- Rate limiting
- API documentation

[Unreleased]: https://github.com/org/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/org/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/org/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/org/repo/releases/tag/v1.0.0
```

## 文档生成工具

### JSDoc/TSDoc

```bash
npx jsdoc -c jsdoc.json
npx typedoc --out docs src/index.ts
```

### Swagger UI

```bash
npx swagger-ui-watcher openapi.yaml
```

### MkDocs

```yaml
site_name: Project Documentation
nav:
  - Home: index.md
  - API Reference: api.md
  - Guide: guide.md
theme:
  name: material
```

## 最佳实践

1. **保持更新**: 代码变更时同步更新文档
2. **示例驱动**: 提供可运行的代码示例
3. **版本化**: 文档与代码版本对应
4. **可搜索**: 提供清晰的导航和搜索
5. **多语言**: 考虑国际化需求
6. **自动化**: 使用工具自动生成API文档

## 相关技能

- [api-design](../code/api-design) - API设计
- [code-generator](../code-generator) - 代码生成
- [backend-python](../../domains/backend/python) - Python后端
- [frontend-react](../../domains/frontend/react) - React开发
