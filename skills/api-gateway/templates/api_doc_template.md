# API文档生成模板

## 一、API文档结构

### 基础信息
```markdown
# API名称

## 概述
简要描述API的功能和用途。

## 基础信息
- **Base URL**: `https://api.example.com/v1`
- **认证方式**: Bearer Token / API Key / OAuth 2.0
- **数据格式**: JSON
- **编码**: UTF-8
```

### 端点文档模板
```markdown
## 端点名称

### 请求
- **方法**: `GET` / `POST` / `PUT` / `DELETE`
- **路径**: `/api/v1/resource`
- **描述**: 详细描述该端点的功能

### 请求参数

#### Headers
| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| Authorization | string | 是 | Bearer {token} |
| Content-Type | string | 是 | application/json |

#### Query Parameters
| 参数名 | 类型 | 必填 | 描述 | 默认值 |
|--------|------|------|------|--------|
| page | integer | 否 | 页码 | 1 |
| limit | integer | 否 | 每页数量 | 20 |

#### Request Body
```json
{
  "field1": "string",  // 描述
  "field2": 123,       // 描述
  "field3": {          // 描述
    "nested": "string"
  }
}
```

### 响应

#### 成功响应 (200 OK)
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "abc123",
    "name": "示例",
    "created_at": "2026-04-09T12:00:00Z"
  }
}
```

#### 错误响应
| 状态码 | 错误码 | 描述 |
|--------|--------|------|
| 400 | INVALID_PARAM | 参数错误 |
| 401 | UNAUTHORIZED | 未授权 |
| 403 | FORBIDDEN | 无权限 |
| 404 | NOT_FOUND | 资源不存在 |
| 500 | INTERNAL_ERROR | 服务器错误 |

### 示例

#### cURL
```bash
curl -X GET "https://api.example.com/v1/resource" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

#### JavaScript
```javascript
const response = await fetch('https://api.example.com/v1/resource', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }
});
const data = await response.json();
```

#### Python
```python
import requests

response = requests.get(
    'https://api.example.com/v1/resource',
    headers={
        'Authorization': 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    }
)
data = response.json()
```
```

## 二、OpenAPI/Swagger模板

```yaml
openapi: 3.0.0
info:
  title: API名称
  description: API描述
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: 生产环境
  - url: https://api-staging.example.com/v1
    description: 测试环境

paths:
  /resource:
    get:
      summary: 获取资源列表
      description: 返回资源列表，支持分页
      tags:
        - Resources
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
          description: 页码
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
          description: 每页数量
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
        '401':
          description: 未授权
        '500':
          description: 服务器错误

components:
  schemas:
    Resource:
      type: object
      properties:
        id:
          type: string
          description: 资源ID
        name:
          type: string
          description: 资源名称
        created_at:
          type: string
          format: date-time
          description: 创建时间

    ResourceList:
      type: object
      properties:
        code:
          type: integer
        message:
          type: string
        data:
          type: array
          items:
            $ref: '#/components/schemas/Resource'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

## 三、错误码规范

### 通用错误码
| 错误码 | 名称 | HTTP状态码 | 描述 |
|--------|------|------------|------|
| 0 | SUCCESS | 200 | 成功 |
| 1001 | INVALID_PARAM | 400 | 参数无效 |
| 1002 | MISSING_PARAM | 400 | 缺少参数 |
| 2001 | UNAUTHORIZED | 401 | 未授权 |
| 2002 | TOKEN_EXPIRED | 401 | Token过期 |
| 2003 | FORBIDDEN | 403 | 无权限 |
| 3001 | NOT_FOUND | 404 | 资源不存在 |
| 4001 | RATE_LIMIT | 429 | 请求过于频繁 |
| 5001 | INTERNAL_ERROR | 500 | 服务器内部错误 |

### 错误响应格式
```json
{
  "code": 1001,
  "message": "参数无效",
  "details": [
    {
      "field": "email",
      "error": "格式不正确"
    }
  ],
  "request_id": "req_abc123",
  "timestamp": "2026-04-09T12:00:00Z"
}
```

## 四、版本管理

### URL版本
```
/api/v1/resource
/api/v2/resource
```

### Header版本
```
Accept: application/json; version=1
```

### 废弃通知
```markdown
## ⚠️ 废弃通知

以下端点已废弃，请迁移到新版本：

| 废弃端点 | 替代端点 | 废弃日期 | 下线日期 |
|----------|----------|----------|----------|
| /api/v1/old | /api/v2/new | 2026-04-01 | 2026-07-01 |
```

## 五、文档生成脚本

```bash
# 从代码生成OpenAPI文档
python3 scripts/generate_openapi.py --output docs/api.yaml

# 生成Markdown文档
python3 scripts/generate_markdown.py --input docs/api.yaml --output docs/api.md

# 生成HTML文档
npx redoc-cli bundle docs/api.yaml -o docs/api.html
```
