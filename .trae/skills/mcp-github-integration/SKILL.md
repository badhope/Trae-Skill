# MCP GitHub Integration

## Description
MCP GitHub 集成专家。帮助实现 MCP 与 GitHub API 的集成，包括仓库管理、Issue 操作、Pull Request 处理等功能。

## Details

### 功能特性
- 仓库操作
- Issue 管理
- Pull Request 处理
- 代码搜索
- 文件操作
- 工作流管理

### 配置

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-personal-access-token"
      }
    }
  }
}
```

### 工具实现

```typescript
import { Octokit } from "@octokit/rest";

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "github_get_repo",
      description: "Get repository information",
      inputSchema: {
        type: "object",
        properties: {
          owner: { type: "string" },
          repo: { type: "string" }
        },
        required: ["owner", "repo"]
      }
    },
    {
      name: "github_list_issues",
      description: "List repository issues",
      inputSchema: {
        type: "object",
        properties: {
          owner: { type: "string" },
          repo: { type: "string" },
          state: { type: "string", enum: ["open", "closed", "all"], default: "open" },
          labels: { type: "array", items: { type: "string" } },
          limit: { type: "integer", default: 30 }
        },
        required: ["owner", "repo"]
      }
    },
    {
      name: "github_create_issue",
      description: "Create a new issue",
      inputSchema: {
        type: "object",
        properties: {
          owner: { type: "string" },
          repo: { type: "string" },
          title: { type: "string" },
          body: { type: "string" },
          labels: { type: "array", items: { type: "string" } },
          assignees: { type: "array", items: { type: "string" } }
        },
        required: ["owner", "repo", "title"]
      }
    },
    {
      name: "github_create_pr",
      description: "Create a pull request",
      inputSchema: {
        type: "object",
        properties: {
          owner: { type: "string" },
          repo: { type: "string" },
          title: { type: "string" },
          head: { type: "string", description: "Branch with changes" },
          base: { type: "string", description: "Branch to merge into" },
          body: { type: "string" },
          draft: { type: "boolean", default: false }
        },
        required: ["owner", "repo", "title", "head", "base"]
      }
    },
    {
      name: "github_search_code",
      description: "Search code in repositories",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string" },
          owner: { type: "string" },
          repo: { type: "string" }
        },
        required: ["query"]
      }
    },
    {
      name: "github_get_file",
      description: "Get file contents",
      inputSchema: {
        type: "object",
        properties: {
          owner: { type: "string" },
          repo: { type: "string" },
          path: { type: "string" },
          ref: { type: "string", description: "Branch or commit SHA" }
        },
        required: ["owner", "repo", "path"]
      }
    },
    {
      name: "github_create_file",
      description: "Create or update a file",
      inputSchema: {
        type: "object",
        properties: {
          owner: { type: "string" },
          repo: { type: "string" },
          path: { type: "string" },
          message: { type: "string", description: "Commit message" },
          content: { type: "string" },
          branch: { type: "string" },
          sha: { type: "string", description: "Required for updating existing file" }
        },
        required: ["owner", "repo", "path", "message", "content", "branch"]
      }
    }
  ]
}));
```

### 工具执行

```typescript
// 获取仓库信息
async function getRepo(owner: string, repo: string) {
  const { data } = await octokit.repos.get({ owner, repo });
  
  return {
    name: data.name,
    fullName: data.full_name,
    description: data.description,
    stars: data.stargazers_count,
    forks: data.forks_count,
    issues: data.open_issues_count,
    language: data.language,
    license: data.license?.spdx_id,
    url: data.html_url
  };
}

// 列出 Issues
async function listIssues(
  owner: string,
  repo: string,
  options: { state?: string; labels?: string[]; limit?: number } = {}
) {
  const { data } = await octokit.issues.listForRepo({
    owner,
    repo,
    state: options.state || "open",
    labels: options.labels?.join(","),
    per_page: options.limit || 30
  });
  
  return data.map(issue => ({
    number: issue.number,
    title: issue.title,
    state: issue.state,
    user: issue.user?.login,
    labels: issue.labels.map(l => typeof l === "string" ? l : l.name),
    createdAt: issue.created_at,
    updatedAt: issue.updated_at,
    url: issue.html_url
  }));
}

// 创建 Issue
async function createIssue(
  owner: string,
  repo: string,
  title: string,
  options: { body?: string; labels?: string[]; assignees?: string[] } = {}
) {
  const { data } = await octokit.issues.create({
    owner,
    repo,
    title,
    body: options.body,
    labels: options.labels,
    assignees: options.assignees
  });
  
  return {
    number: data.number,
    title: data.title,
    url: data.html_url
  };
}

// 创建 Pull Request
async function createPR(
  owner: string,
  repo: string,
  title: string,
  head: string,
  base: string,
  options: { body?: string; draft?: boolean } = {}
) {
  const { data } = await octokit.pulls.create({
    owner,
    repo,
    title,
    head,
    base,
    body: options.body,
    draft: options.draft
  });
  
  return {
    number: data.number,
    title: data.title,
    state: data.state,
    url: data.html_url
  };
}

// 搜索代码
async function searchCode(query: string, options: { owner?: string; repo?: string } = {}) {
  let q = query;
  if (options.owner && options.repo) {
    q += ` repo:${options.owner}/${options.repo}`;
  } else if (options.owner) {
    q += ` user:${options.owner}`;
  }
  
  const { data } = await octokit.search.code({
    q,
    per_page: 30
  });
  
  return data.items.map(item => ({
    name: item.name,
    path: item.path,
    repository: item.repository.full_name,
    url: item.html_url
  }));
}

// 获取文件内容
async function getFile(
  owner: string,
  repo: string,
  path: string,
  ref?: string
) {
  const { data } = await octokit.repos.getContent({
    owner,
    repo,
    path,
    ref
  });
  
  if (Array.isArray(data)) {
    return data.map(item => ({
      name: item.name,
      path: item.path,
      type: item.type
    }));
  }
  
  if (data.type === "file") {
    const content = Buffer.from(data.content, "base64").toString("utf-8");
    return {
      name: data.name,
      path: data.path,
      size: data.size,
      content,
      sha: data.sha
    };
  }
  
  throw new Error("Not a file");
}

// 创建或更新文件
async function createFile(
  owner: string,
  repo: string,
  path: string,
  message: string,
  content: string,
  branch: string,
  sha?: string
) {
  const { data } = await octokit.repos.createOrUpdateFileContents({
    owner,
    repo,
    path,
    message,
    content: Buffer.from(content).toString("base64"),
    branch,
    sha
  });
  
  return {
    commit: {
      sha: data.commit.sha,
      message: data.commit.message,
      url: data.commit.html_url
    }
  };
}
```

### 资源暴露

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  // 获取用户仓库列表
  const { data: repos } = await octokit.repos.listForAuthenticatedUser({
    per_page: 100
  });
  
  return {
    resources: repos.map(repo => ({
      uri: `github://${repo.full_name}`,
      name: repo.full_name,
      description: repo.description || undefined,
      mimeType: "application/json"
    }))
  };
});

server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => ({
  resourceTemplates: [
    {
      uriTemplate: "github://{owner}/{repo}",
      name: "Repository",
      mimeType: "application/json"
    },
    {
      uriTemplate: "github://{owner}/{repo}/issues/{number}",
      name: "Issue",
      mimeType: "application/json"
    },
    {
      uriTemplate: "github://{owner}/{repo}/pulls/{number}",
      name: "Pull Request",
      mimeType: "application/json"
    },
    {
      uriTemplate: "github://{owner}/{repo}/blob/{branch}/{path}",
      name: "File",
      mimeType: "text/plain"
    }
  ]
}));
```

### Webhook 处理

```typescript
import { createNodeMiddleware } from "@octokit/webhooks";
import { Webhooks } from "@octokit/webhooks";

const webhooks = new Webhooks({
  secret: process.env.GITHUB_WEBHOOK_SECRET!
});

webhooks.on("issues.opened", async ({ payload }) => {
  // 处理新 Issue
  console.log(`New issue: ${payload.issue.title}`);
});

webhooks.on("pull_request.opened", async ({ payload }) => {
  // 处理新 PR
  console.log(`New PR: ${payload.pull_request.title}`);
});

webhooks.on("push", async ({ payload }) => {
  // 处理 Push 事件
  console.log(`Push to ${payload.ref}`);
});
```

### 权限控制

```typescript
class GitHubPermissionManager {
  private allowedRepos: Set<string>;
  private allowedOrgs: Set<string>;
  
  constructor(config: {
    allowedRepos?: string[];
    allowedOrgs?: string[];
  }) {
    this.allowedRepos = new Set(config.allowedRepos || []);
    this.allowedOrgs = new Set(config.allowedOrgs || []);
  }
  
  canAccess(owner: string, repo: string): boolean {
    if (this.allowedRepos.size === 0 && this.allowedOrgs.size === 0) {
      return true;
    }
    
    const fullName = `${owner}/${repo}`;
    
    return this.allowedRepos.has(fullName) || this.allowedOrgs.has(owner);
  }
  
  canWrite(owner: string, repo: string): boolean {
    // 写权限需要更严格的检查
    return this.canAccess(owner, repo);
  }
}
```

### 最佳实践

1. **Token 安全**: 使用最小权限的 Personal Access Token
2. **速率限制**: 遵守 GitHub API 速率限制
3. **缓存**: 缓存频繁访问的数据
4. **错误处理**: 处理 API 错误和重试
5. **Webhook 验证**: 验证 Webhook 签名

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `git-operations` - Git 操作
- `ci-cd-pipeline` - CI/CD 流水线
- `api-integrator` - API 集成
