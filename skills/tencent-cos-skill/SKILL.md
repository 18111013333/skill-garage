---
name: tencent-cloud-cos
description: >
  腾讯云对象存储(COS)和数据万象(CI)集成技能。覆盖文件存储管理、AI处理和知识库三大核心场景。
  存储场景：上传文件到云端、下载云端文件、批量管理存储桶文件、获取文件签名链接分享、查看文件元信息。
  图片处理场景：图片质量评估打分、AI超分辨率放大、AI智能裁剪、二维码/条形码识别、添加文字水印、获取图片EXIF信息、
  缩放、裁剪、旋转、格式转换。
  文档处理场景：Word/Excel/PPT等办公文档转PDF、文档预览。
  媒体处理场景：视频智能封面提取、视频转码、视频截帧、获取媒体信息。
  内容审核场景：图片/视频/音频/文本/文档内容审核，检测违规内容。
  智能语音场景：语音识别（音频转文字）、语音合成（文字转语音）、音频降噪、人声分离。
  文件处理场景：文件哈希计算、文件压缩打包、文件解压。
  内容识别场景：图片标签识别、OCR文字识别。
  知识库场景：一键创建知识库、上传文档到知识库、从知识库检索内容片段。
  智能检索场景：MetaInsight以图搜图、以文搜图、人脸搜索、元数据检索、多模态文档检索。
  当用户提到以下关键词或口语化表述时应触发此技能：
  上传到COS、腾讯云存储、对象存储、云存储、存储桶、Bucket、
  图片处理、图片压缩、图片放大、超分辨率、抠图、裁剪、二维码识别、水印、
  文档转换、转PDF、视频封面、智能封面、以图搜图、图片搜索、MetaInsight、
  COS上传、COS下载、签名URL、腾讯云文件、数据万象、CI处理、
  内容审核、图片审核、视频审核、文本审核、语音识别、语音合成、降噪、人声分离、
  OCR、文字识别、图片标签、
  创建知识库、建一个知识库、上传到知识库、往知识库里加文件、查询知识库、
  从知识库找、搜索知识库、知识库检索、文档检索、文档搜索。
  即使用户没有明确提到COS或腾讯云，只要涉及"把文件传到云上"、"生成下载链接"、
  "处理云端图片"、"帮我建个知识库"、"把文档放进知识库"、"从知识库里搜一下"、
  "加密COS凭证"、"COS密钥不安全"、"加密一下COS密钥"、"保护COS密钥"等意图，也应该触发此技能。
description_zh: "腾讯云 COS 对象存储、数据万象数据智能处理、MetaInsight多模态检索、知识库搭建"
description_en: "Tencent Cloud COS Object Storage, CI Data Intelligence Processing, MetaInsight Multi-modal Retrieval, Knowledge Base Setup"
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires":
          {
            "secrets":
              [
                "SecretId",
                "SecretKey"
              ],
            "optionalSecrets":
              [
                "Token"
              ],
            "config":
              [
                "Region",
                "Bucket"
              ],
            "optionalConfig":
              [
                "DatasetName",
                "Domain",
                "ServiceDomain",
                "Protocol"
              ],
            "envMapping":
              {
                "SecretId": "TENCENT_COS_SECRET_ID",
                "SecretKey": "TENCENT_COS_SECRET_KEY",
                "Token": "TENCENT_COS_TOKEN",
                "Region": "TENCENT_COS_REGION",
                "Bucket": "TENCENT_COS_BUCKET",
                "DatasetName": "TENCENT_COS_DATASET_NAME",
                "Domain": "TENCENT_COS_DOMAIN",
                "ServiceDomain": "TENCENT_COS_SERVICE_DOMAIN",
                "Protocol": "TENCENT_COS_PROTOCOL"
              },
            "secretsDescription":
              {
                "SecretId":
                  {
                    "label": "腾讯云 API 密钥 ID",
                    "type": "cloud-credential",
                    "provider": "Tencent Cloud",
                    "sensitivity": "critical",
                    "scope": "COS object storage and CI data processing APIs"
                  },
                "SecretKey":
                  {
                    "label": "腾讯云 API 密钥 Key",
                    "type": "cloud-credential",
                    "provider": "Tencent Cloud",
                    "sensitivity": "critical",
                    "scope": "COS object storage and CI data processing APIs"
                  },
                "Token":
                  {
                    "label": "STS 临时安全令牌",
                    "type": "session-token",
                    "provider": "Tencent Cloud STS",
                    "sensitivity": "high",
                    "scope": "Time-limited access (default 1800s), auto-expires"
                  }
              }
          },
        "security":
          {
            "credentialStorage":
              {
                "default": "ephemeral",
                "ephemeral":
                  {
                    "description": "Credentials exist only in shell session environment variables; nothing written to disk",
                    "persistsToDisk": false,
                    "recommendation": "RECOMMENDED — use with STS temporary credentials"
                  }
              },
            "requirements": [
              "MUST use sub-account keys with least-privilege COS-only policy; root account keys are FORBIDDEN",
              "STS temporary credentials are recommended; default behavior is ephemeral (no disk persistence)",
              "Credentials are NEVER echoed back to the user in chat"
            ]
          },
        "install":
          [
            {
              "id": "node-cos-sdk",
              "kind": "node",
              "package": "cos-nodejs-sdk-v5",
              "label": "Install COS Node.js SDK"
            }
          ]
      }
  }
---

# 腾讯云 COS 技能

一站式管理腾讯云对象存储(COS)和数据万象(CI)，通过统一的 Node.js SDK 脚本提供以下能力：

- **文件存储**：上传、下载、列出、删除文件，获取签名下载链接，批量操作，复制
- **存储桶管理**：列出/创建存储桶，ACL、跨域、标签、版本控制、生命周期管理
- **图片处理**：缩放、裁剪、旋转、格式转换、文字水印、质量评估、超分辨率、智能裁剪、二维码识别
- **内容识别**：图片标签识别、OCR 文字识别
- **文档处理**：办公文档转 PDF、文档预览（图片/HTML）
- **媒体处理**：视频智能封面、转码、截帧、媒体信息
- **内容审核**：图片/视频/音频/文本/文档违规检测
- **智能语音**：语音识别、语音合成、音频降噪、人声分离
- **文件处理**：哈希计算、压缩、解压
- **智能检索 MetaInsight**：数据集管理、索引管理、以图搜图、文本搜图、人脸搜索、元数据检索、多模态文档检索
- **🚀 知识库**：一键创建知识库（自动创建桶+数据集+绑定），上传文档到知识库，语义检索知识库内容

所有操作通过 `scripts/cos_node.mjs` 单一脚本完成，输出 JSON 格式。

## 首次使用 — 自动设置

当用户首次要求操作 COS 时，按以下流程操作：

### 步骤 1：检查当前状态

```bash
{baseDir}/scripts/setup.sh --check-only
```

如果 Node.js 和 cos-nodejs-sdk-v5 已安装、环境变量已配置，跳到「操作指南」。

### 步骤 2：如果未配置，引导用户提供凭证

告诉用户：
> 我需要你的腾讯云凭证来连接 COS 存储服务。请放心，你的密钥会受到以下保护：
>
> #### 🛡️ 凭证安全保障
> - **默认不落盘**：凭证仅存于当前终端会话内存中，关闭终端即消失
> - **可选持久化**：如需保存，凭证写入项目本地 `.env` 文件（仅当前用户可读，权限 600）
> - **支持 AES-256 加密**：持久化后可一键加密为 `.env.enc`，明文自动删除，密钥绑定本机+本用户，拷贝到其他环境无法解密
> - **自动防误提交**：`.env` / `.env.enc` 自动添加到 `.gitignore`，不会进入版本控制
> - **永远不会在对话中回显你的密钥**
>
> #### 🔒 推荐方案：STS 临时凭证（最安全，自带有效期）
> 1. **SecretId** — TmpSecretId
> 2. **SecretKey** — TmpSecretKey
> 3. **Token** — SecurityToken
> 4. **Region** — 存储桶区域（如 ap-guangzhou）
> 5. **Bucket** — 存储桶名称（格式 name-appid）
>
> #### ⚠️ 降级方案：永久密钥（必须使用子账号最小权限密钥）
> 1. **SecretId** / **SecretKey** / **Region** / **Bucket**
>
> #### 可选配置
> - **DatasetName** — 数据万象数据集名称（仅 MetaInsight 检索需要）
> - **Domain** / **ServiceDomain** / **Protocol** — 自定义域名配置

### 步骤 3：设置环境变量并运行安装

```bash
export TENCENT_COS_SECRET_ID="<SecretId>"
export TENCENT_COS_SECRET_KEY="<SecretKey>"
export TENCENT_COS_TOKEN="<Token>"  # STS 临时凭证才需要
export TENCENT_COS_REGION="<Region>"
export TENCENT_COS_BUCKET="<Bucket>"

# 默认模式：凭证仅存于当前 session，关闭终端后需重新 export
{baseDir}/scripts/setup.sh --from-env

# 持久化模式：凭证写入项目本地 .env 文件，下次自动读取
{baseDir}/scripts/setup.sh --from-env --persist
```

