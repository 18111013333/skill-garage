- DOCX：{docx_path}

分享链接：
{share_url}
```

字段映射规则：
- `{title}` = 脚本返回的 `title`
- `{content}` = 脚本返回的 `content`
- `{pdf_path}` = `attachments` 中 `type=PDF` 对应的 `url`
- `{docx_path}` = `attachments` 中 `type=DOCX` 对应的 `url`
- `{share_url}` = 脚本返回的 `share_url`

当附件缺失时：
- 若仅有一种格式，仅输出存在的那一行（PDF 或 DOCX）。
- 若两种都不存在，输出：`完整报告：暂无可用附件`

## 语言要求

始终优先中文输出。若用户使用其他语言，可在交互提示中适度双语，但报告正文与字段含义保持中文语境。

## 使用约束与建议

- 不要在 skill 层重写脚本已生成的 `content` 主体结构，避免与脚本逻辑漂移。
- 除附件路径展示外，不在 skill 层追加二次总结，正文以脚本 `content` 结果为准。
- 若脚本返回 `ok=false`，优先透传 `message`；不要自行编造错误原因。
- 该 skill 目标是“生成并返回结果”，不是在 skill 内追加长篇二次分析。

## 常见错误处理：
- 缺少 query：`BAD_REQUEST`，message 为“缺少 query 参数”。
- 不支持实体：`ERROR_ENTITY`，message 为“目前暂不支持此类实体体进行分析。”
- 网络/超时/服务异常：`TIMEOUT` / `NETWORK_ERROR` / `HTTP_ERROR` / `UNEXPECTED_ERROR`，对用户统一提示“报告生成服务暂时不可用，请稍后重试。”。

错误输出强约束：
- 只要接口响应或脚本标准输出（print 的 JSON）中存在 `message` 字段，模型必须输出该 `message`，不得省略、不得改写、不得替换为其他话术。
- 当 `ok=false` 时，优先输出错误 `message`；若同时存在 `error_code`，可附带展示 `error_code`，但不影响 `message` 原样透传。
