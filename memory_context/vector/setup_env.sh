#!/bin/bash
# Embedding 环境变量配置脚本

# API Keys
export API_TOKEN="JEHMRUUDOKBQQLCSWIIA0EYHKDZJ3KORM2NEVLPM"
export GITEE_AI_API_KEY="JEHMRUUDOKBQQLCSWIIA0EYHKDZJ3KORM2NEVLPM"

# 验证
echo "环境变量已配置:"
echo "  API_TOKEN=$API_TOKEN"
echo "  GITEE_AI_API_KEY=$GITEE_AI_API_KEY"

# 测试连接
echo ""
echo "测试 API 连接..."
python3 -c "
from openai import OpenAI
import os

client = OpenAI(
    base_url='https://ai.gitee.com/v1',
    api_key=os.environ.get('API_TOKEN'),
    default_headers={'X-Failover-Enabled': 'true'}
)

response = client.embeddings.create(
    input='测试文本',
    model='Qwen3-Embedding-8B',
    dimensions=4096
)

print(f'✅ API 连接成功！向量维度: {len(response.data[0].embedding)}')
"
