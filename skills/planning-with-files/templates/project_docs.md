# 项目文档模板

## 一、README模板

```markdown
# 项目名称

简短的项目描述，一句话说明项目是什么。

## 功能特性

- 特性1
- 特性2
- 特性3

## 快速开始

### 环境要求

- Node.js >= 16.0.0
- Python >= 3.8
- Docker (可选)

### 安装

\`\`\`bash
# 克隆项目
git clone https://github.com/username/project.git

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
\`\`\`

### 运行

\`\`\`bash
# 开发模式
npm run dev

# 生产模式
npm start
\`\`\`

## 项目结构

\`\`\`
project/
├── src/              # 源代码
│   ├── components/   # 组件
│   ├── services/     # 服务
│   └── utils/        # 工具函数
├── tests/            # 测试
├── docs/             # 文档
└── config/           # 配置
\`\`\`

## 技术栈

- 前端：React, TypeScript
- 后端：Node.js, Express
- 数据库：PostgreSQL
- 缓存：Redis

## API文档

详见 [API文档](./docs/api.md)

## 贡献指南

详见 [贡献指南](./CONTRIBUTING.md)

## 许可证

MIT License
```

## 二、CHANGELOG模板

```markdown
# 更新日志

本项目的所有重要变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增
- 待发布的新功能

### 变更
- 待发布的变更

### 修复
- 待发布的修复

## [1.2.0] - 2026-04-09

### 新增
- 添加用户导出功能
- 支持批量操作
- 新增API限流

### 变更
- 优化查询性能
- 更新UI样式

### 修复
- 修复登录超时问题
- 修复数据导出格式错误

### 移除
- 移除废弃的API接口

## [1.1.0] - 2026-03-15

### 新增
- 添加用户权限管理
- 支持多语言

### 修复
- 修复分页显示问题

## [1.0.0] - 2026-02-01

### 新增
- 首次发布
- 基础用户管理功能
- 基础API接口
```

## 三、CONTRIBUTING模板

```markdown
# 贡献指南

感谢你考虑为本项目做出贡献！

## 行为准则

本项目采用贡献者公约作为行为准则。

## 如何贡献

### 报告Bug

1. 检查是否已有相同问题的Issue
2. 使用Issue模板创建新Issue
3. 详细描述问题：复现步骤、期望结果、实际结果

### 提交功能建议

1. 创建Feature Request Issue
2. 描述功能需求和使用场景
3. 等待维护者反馈

### 提交代码

1. Fork本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'feat: 添加某功能'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建Pull Request

## 开发指南

### 环境搭建

\`\`\`bash
npm install
cp .env.example .env
npm run dev
\`\`\`

### 代码规范

- 遵循ESLint规则
- 使用Prettier格式化
- 提交信息遵循Conventional Commits

### 测试

\`\`\`bash
# 运行测试
npm test

# 测试覆盖率
npm run coverage
\`\`\`

### 文档

- 更新相关文档
- API变更需更新API文档
- 新功能需更新README

## Pull Request流程

1. 确保所有测试通过
2. 确保代码符合规范
3. 更新相关文档
4. 填写PR模板
5. 等待代码审查

## 许可证

提交代码即表示你同意你的代码将以项目的许可证发布。
```

## 四、API文档模板

```markdown
# API文档

## 基础信息

- Base URL: `https://api.example.com/v1`
- 认证方式: Bearer Token
- 数据格式: JSON

## 认证

### 获取Token

**请求**
\`\`\`
POST /auth/token
\`\`\`

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**响应**
\`\`\`json
{
  "code": 0,
  "data": {
    "token": "xxx",
    "expires_in": 3600
  }
}
\`\`\`

## 用户接口

### 获取用户列表

**请求**
\`\`\`
GET /users
\`\`\`

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| limit | int | 否 | 每页数量，默认20 |

**响应**
\`\`\`json
{
  "code": 0,
  "data": {
    "list": [...],
    "total": 100,
    "page": 1,
    "limit": 20
  }
}
\`\`\`

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 参数错误 |
| 2001 | 未授权 |
| 3001 | 资源不存在 |
| 5001 | 服务器错误 |
```

## 五、架构文档模板

```markdown
# 系统架构文档

## 1. 概述

### 1.1 项目背景
描述项目的背景和目标。

### 1.2 系统目标
- 目标1
- 目标2

## 2. 系统架构

### 2.1 整体架构

\`\`\`
┌─────────────────────────────────────┐
│           客户端层                   │
│  Web App  │  Mobile App  │  API     │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│           网关层                     │
│  API Gateway  │  Load Balancer      │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│           服务层                     │
│  User Service  │  Order Service     │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│           数据层                     │
│  PostgreSQL  │  Redis  │  S3        │
└─────────────────────────────────────┘
\`\`\`

### 2.2 技术选型

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | React | UI框架 |
| 后端 | Node.js | 运行时 |
| 数据库 | PostgreSQL | 主数据库 |
| 缓存 | Redis | 缓存层 |

## 3. 模块设计

### 3.1 用户模块
- 功能：用户注册、登录、权限管理
- 接口：/api/users/*

### 3.2 订单模块
- 功能：订单创建、查询、状态管理
- 接口：/api/orders/*

## 4. 数据设计

### 4.1 ER图

\`\`\`
User ──┬── Order
       │
       └── Profile
\`\`\`

### 4.2 主要表结构

#### users表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | bigint | 主键 |
| username | varchar | 用户名 |
| email | varchar | 邮箱 |

## 5. 部署架构

### 5.1 生产环境

\`\`\`
Internet → CDN → ALB → ECS → RDS
\`\`\`

### 5.2 CI/CD流程

\`\`\`
Code → Build → Test → Deploy → Monitor
\`\`\`
```

## 六、Issue模板

### Bug报告
```markdown
## Bug描述
简洁清晰地描述bug。

## 复现步骤
1. 打开 '...'
2. 点击 '...'
3. 滚动到 '...'
4. 看到错误

## 期望行为
描述你期望发生的事情。

## 实际行为
描述实际发生的事情。

## 截图
如果有截图，请附上。

## 环境
- OS: [e.g. macOS, Windows]
- Browser: [e.g. Chrome, Safari]
- Version: [e.g. 1.0.0]

## 其他信息
其他相关信息。
```

### 功能请求
```markdown
## 功能描述
清晰描述你希望添加的功能。

## 使用场景
描述这个功能的使用场景。

## 建议方案
如果有建议的实现方案，请描述。

## 替代方案
描述你考虑过的替代方案。

## 其他信息
其他相关信息。
```
