# 用户画像提取规则

## 自动提取规则

### 偏好提取

| 用户表达模式 | 提取类型 | 示例 |
|-------------|---------|------|
| "我喜欢/偏好/习惯..." | 偏好声明 | "我喜欢简洁的回答" → output_style: concise |
| "不要/别/不喜欢..." | 负面偏好 | "不要用感叹号" → avoid: exclamation_marks |
| "以后/总是/每次..." | 长期偏好 | "以后直接给代码" → default_action: code_first |
| "这次/暂时/先..." | 临时偏好 | "这次详细点" → temp: detailed |

### 技术画像提取

| 用户表达模式 | 提取类型 | 示例 |
|-------------|---------|------|
| 提及技术/框架 | 技术栈 | "用 React 做" → tech_stack: React |
| 提及工具/平台 | 工具偏好 | "用 VS Code" → editor: VS Code |
| 技术问题深度 | 技能水平 | 深度问题 → level: advanced |
| 专业术语使用 | 领域识别 | 使用架构术语 → domain: architecture |

### 场景识别规则

| 关键词/模式 | 场景类型 |
|------------|---------|
| 代码、调试、部署、API | work.coding |
| 文档、报告、写作、文章 | work.writing |
| 研究、调研、分析、学习 | learning.research |
| 会议、日程、提醒、计划 | life.planning |
| 设计、创意、灵感、创作 | creative.design |

### 情绪/状态提取

| 表达模式 | 状态标签 |
|---------|---------|
| 急促、催促、快点 | urgent |
| 详细解释、慢慢来 | patient |
| 纠正、不对、错了 | correcting |
| 感谢、很好、不错 | satisfied |
| 困惑、不懂、怎么 | confused |

## 提取优先级

1. **显式声明** - 用户明确说"记住..."、"以后..."
2. **纠正行为** - 用户纠正 AI 的输出
3. **重复模式** - 多次出现的相同偏好
4. **单次表达** - 仅出现一次的偏好

## 画像更新触发条件

### 立即更新 (L3)
- 用户显式声明
- 用户纠正同一问题 2 次以上
- 涉及核心身份信息

### 延迟更新 (L2 → L3)
- 同一偏好在不同场景出现 3 次以上
- 周期性回顾时发现稳定模式

### 不更新
- 临时性表达 ("这次...")
- 情绪性表达 (不反映长期偏好)
- 矛盾信息 (需要进一步观察)

## 隐私保护

### 不提取的内容
- 具体的密码、密钥
- 完整的身份证号、银行卡号
- 详细的住址信息
- 他人的隐私信息

### 脱敏规则
- 手机号: 保留前 3 后 4 位
- 邮箱: 保留用户名前 3 字符
- 地址: 只保留城市级别
- 姓名: 可用昵称替代

## 提取示例

### 输入
```
用户: "帮我写个 Python 脚本处理 CSV，不要用 pandas，用标准库就行。
      以后写代码都这样，直接给代码，别解释太多。"
```

### 提取结果
```yaml
L1 (会话):
  current_task: write_python_script
  task_context: csv_processing
  temp_preferences: {}

L2 (场景 - work.coding):
  language_preference: Python
  library_preference: stdlib_over_pandas
  output_preference: code_first

L3 (长期):
  coding_style:
    language: Python
    approach: minimal_dependencies
  interaction_style:
    output: code_first
    explanation: minimal
```
