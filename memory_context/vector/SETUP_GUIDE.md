# Embedding 环境配置指南

## 当前状态

```
❌ API Key 无效 (401 Unauthorized)
```

## 获取新的 API Key

### 步骤

1. **访问 Gitee AI**
   - 网址: https://ai.gitee.com

2. **登录账号**
   - 使用 Gitee 账号登录

3. **创建访问令牌**
   - 进入「API 管理」或「访问令牌」页面
   - 点击「创建令牌」
   - 复制生成的 API Key

4. **配置环境变量**

   ```bash
   # 方式1：临时设置（推荐先测试）
   export API_TOKEN="你的新API Key"
   export GITEE_AI_API_KEY="你的新API Key"

   # 测试
   python3 test_embedding.py
   ```

   ```bash
   # 方式2：永久设置
   # 编辑配置文件
   nano ~/.bashrc

   # 添加以下行
   export API_TOKEN="你的新API Key"
   export GITEE_AI_API_KEY="你的新API Key"

   # 使配置生效
   source ~/.bashrc
   ```

5. **验证配置**

   ```bash
   # 检查环境变量
   echo $API_TOKEN

   # 运行测试
   cd ~/.openclaw/workspace/vector
   python3 test_embedding.py
   ```

## 免费额度

- 每日免费: 100 次
- 重置时间: 每日 0:00

## 支持的维度

| 维度 | 精度 | 速度 | 推荐场景 |
|------|------|------|----------|
| 1024 | 高 | 快 | 一般应用 |
| 2048 | 很高 | 中 | 高精度需求 |
| 4096 | 极高 | 中 | 最高精度需求 |

## 故障排查

### 401 Unauthorized
- API Key 无效或过期
- 需要重新获取

### 429 Too Many Requests
- 超过免费额度
- 等待次日重置

### Connection Error
- 网络问题
- 检查网络连接

## 配置文件位置

```
~/.openclaw/.env.embedding
~/.openclaw/workspace/vector/setup_env.sh
```

## 下一步

获取新的 API Key 后，告诉我，我会帮你更新配置。
