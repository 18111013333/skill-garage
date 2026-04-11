---
name: xiaoyi-image-understanding
description: 使用小艺图像理解API进行图像内容识别和描述，获取图像的详细文本描述
---

# 小艺图像理解 Skill

## 简介
通过小艺图像理解 API 对图像进行智能分析，自动生成详细的图像描述，识别图像中的对象、场景、文字等内容。

## 特性
- ✅ **开箱即用** - 配置已固化，无需手动设置
- ✅ **流式响应** - 支持 SSE 实时流式返回
- ✅ **智能识别** - 精准识别图像内容和细节
- ✅ **文件上传** - 支持将本地图片上传到云存储，获取可访问的 URL
- ✅ **中文优化** - 适合中文描述场景
- ✅ **简洁输出** - 直接打印结果供大模型读取

## 文件结构
```
xiaoyi-image-understanding/
├── SKILL.md                # 使用说明（本文档）
├── scripts                 # 程序文件夹
│ ├── image_understanding.py # 主程序（图像理解）
│ └── file_upload.py         # 文件上传脚本（本地图片 → 云存储 URL）
├── _meta.json              # Skill 元数据
└── package.json            # 项目配置
```

## 使用方法

### 图像理解（直接使用公网 URL）

```bash
# 进入 skill 目录
cd /home/sandbox/.openclaw/workspace/skills/xiaoyi-image-understanding

# 基本使用
python ./scripts/image_understanding.py "https://example.com/image.jpg"

# 自定义提示词
python ./scripts/image_understanding.py "https://example.com/image.jpg" "详细描述这张图片"

# 开启调试模式
python ./scripts/image_understanding.py "https://example.com/image.jpg" --debug
```

### 本地图片上传 + 图像理解（两步流程）

当图片在本地、无公网 URL 时，先上传获取 URL，再执行图像理解：

```bash
# 步骤 1：上传本地图片，获取文件 URL
python ./scripts/file_upload.py "/path/to/local/image.jpg"
# 输出示例：{"objectId": "D4EV1DFka-XQFGvYdUIcIJXhg", "fileUrl": "https://obs.example.com/osms/...", "fileName": "image.jpg"}

# 步骤 2：使用返回的 fileUrl 进行图像理解
python ./scripts/image_understanding.py "https://obs.example.com/osms/..."
```

也可以在 Python 代码中串联调用：

```python
from scripts.file_upload import upload_file
from scripts.image_understanding import image_understanding

# 上传本地图片
upload_result = upload_file('/path/to/image.jpg')
if upload_result:
    # 使用返回的 fileUrl 进行图像理解
    result = image_understanding(upload_result['fileUrl'], '描述这张图片')
    print(result)
    # 输出: {"caption": "图片描述文本..."}
```

## API 信息

| 项目 | 值 |
|------|-----|
| 图像理解地址 | `https://hag-drcn.op.dbankcloud.com/celia-claw/v1/sse-api/skill/execute` |

## 详细文档

请参阅 [references/details.md](references/details.md)
