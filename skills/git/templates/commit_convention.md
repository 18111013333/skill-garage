# Git提交规范模板

## 一、提交信息格式

### 基本格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型说明
| 类型 | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat(user): 添加用户登录功能 |
| fix | 修复bug | fix(api): 修复接口超时问题 |
| docs | 文档更新 | docs(readme): 更新安装说明 |
| style | 代码格式 | style: 格式化代码缩进 |
| refactor | 重构 | refactor(auth): 重构认证逻辑 |
| perf | 性能优化 | perf(db): 优化查询性能 |
| test | 测试 | test(user): 添加登录测试用例 |
| chore | 构建/工具 | chore: 更新依赖版本 |
| revert | 回滚 | revert: 回滚上次提交 |
| ci | CI配置 | ci: 添加GitHub Actions配置 |

### 作用域示例
- `feat(user):` - 用户模块
- `fix(api):` - API模块
- `docs(readme):` - README文档
- `style(css):` - CSS样式
- `refactor(core):` - 核心模块

## 二、提交信息规范

### 标题行规范
- 使用祈使句，现在时态
- 首字母小写
- 不以句号结尾
- 长度不超过50字符

**正确示例：**
```
feat(user): 添加用户注册功能
fix(api): 修复响应数据格式错误
docs: 更新API文档
```

**错误示例：**
```
添加了用户注册功能  # 缺少类型
Feat(user): 添加用户注册功能  # 大写
feat(user): 添加用户注册功能。  # 有句号
feat(user): 添加了一个新的用户注册功能，支持邮箱和手机号  # 太长
```

### 正文规范
- 使用祈使句
- 说明"做了什么"和"为什么"
- 可以分点列出

**示例：**
```
feat(user): 添加用户注册功能

- 支持邮箱注册
- 支持手机号注册
- 添加验证码验证
- 密码加密存储

Closes #123
```

### 页脚规范
- 关联Issue：`Closes #123` 或 `Fixes #123`
- Breaking Changes：`BREAKING CHANGE: 描述`

**示例：**
```
feat(api): 重构API响应格式

BREAKING CHANGE: API响应格式从 {code, data} 改为 {status, result}

Closes #456
```

## 三、提交模板

### 功能开发
```
feat(<module>): <功能描述>

- 功能点1
- 功能点2
- 功能点3

测试：
- 测试用例1
- 测试用例2

Closes #<issue_number>
```

### Bug修复
```
fix(<module>): <bug描述>

问题：
- 问题描述

原因：
- 根本原因

解决方案：
- 修复方法

测试：
- 验证方法

Fixes #<issue_number>
```

### 重构
```
refactor(<module>): <重构描述>

重构内容：
- 重构点1
- 重构点2

影响范围：
- 影响模块1
- 影响模块2

测试：
- 回归测试结果
```

## 四、分支命名规范

### 分支类型
| 类型 | 格式 | 示例 |
|------|------|------|
| 功能 | feature/<name> | feature/user-login |
| 修复 | fix/<name> | fix/api-timeout |
| 发布 | release/<version> | release/v1.2.0 |
| 热修复 | hotfix/<name> | hotfix/security-patch |

### 命名规则
- 使用小写字母
- 使用连字符分隔
- 简洁明了
- 包含Issue编号（可选）

**示例：**
```
feature/user-authentication
feature/#123-payment-integration
fix/api-response-format
hotfix/security-vulnerability
```

## 五、工作流规范

### Git Flow
```
main (生产分支)
  └── develop (开发分支)
        ├── feature/xxx (功能分支)
        ├── feature/yyy
        └── ...
              ↓ 合并到 develop
        release/v1.0.0 (发布分支)
              ↓ 合并到 main
        hotfix/xxx (热修复分支)
              ↓ 合并到 main 和 develop
```

### 提交频率
- 小步提交，频繁提交
- 每个提交应该是一个完整的逻辑单元
- 避免一次提交多个不相关的改动

### 提交前检查
- [ ] 代码已测试
- [ ] 无语法错误
- [ ] 无敏感信息
- [ ] 提交信息格式正确
- [ ] 关联正确的Issue

## 六、工具配置

### Git Hooks
```bash
# .git/hooks/commit-msg
#!/bin/sh
commit_msg=$(cat "$1")
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore|revert|ci)(\(.+\))?: .{1,50}"; then
    echo "错误: 提交信息格式不正确"
    echo "格式: <type>(<scope>): <subject>"
    exit 1
fi
```

### Commitlint配置
```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'chore', 'revert', 'ci'
    ]],
    'subject-max-length': [2, 'always', 50],
    'body-max-line-length': [2, 'always', 72]
  }
};
```

### Husky配置
```json
// package.json
{
  "husky": {
    "hooks": {
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS",
      "pre-commit": "lint-staged"
    }
  }
}
```

## 七、常见问题

### 修改上次提交信息
```bash
git commit --amend -m "新的提交信息"
```

### 合并多个提交
```bash
git rebase -i HEAD~3
# 将 pick 改为 squash
```

### 撤销提交
```bash
# 保留改动
git reset --soft HEAD~1

# 丢弃改动
git reset --hard HEAD~1
```
