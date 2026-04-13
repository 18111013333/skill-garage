然后根据系统执行对应的命令：

**macOS：**
```bash
source ~/.zshrc
```

**Linux：**
```bash
source ~/.bashrc
```

### 3. 安装依赖


```bash
pip3 install httpx --user
```

## 快速开始

### 1. 命令行调用

```bash
python3 {baseDir}/scripts/get_data.py --query 股价大于100元，主力流入，成交额排名前50 --select-type A股
```

**输出示例**
```
CSV: /path/to/miaoxiang/mx_stocks_screener/mx_stocks_screener_9535fe18.csv
描述: /path/to/miaoxiang/mx_stocks_screener/mx_stocks_screener_9535fe18_description.txt
行数: 42
```

**参数说明：**

| 参数 | 说明 | 必填 |
|------|------|------|
| `--query` | 自然语言查询条件 | ✅ |
| `--select-type` | 查询领域 | ✅ |

### 2. 代码调用

```python
import asyncio
from pathlib import Path
from scripts.get_data import query_mx_stocks_screener

async def main():
    result = await query_mx_stocks_screener(
        query="A股半导体板块市值前20",
        selectType="A股",
        output_dir=Path("miaoxiang/mx_stocks_screener"),
    )
    if "error" in result:
        print(result["error"])
    else:
        print(result["csv_path"], result["row_count"])

asyncio.run(main())
```

## 输出文件说明

| 文件 | 说明 |
|------|------|
| `mx_stocks_screener_<查询ID>.csv` | 全量数据表，列名为**中文**（由返回的 columns 映射），UTF-8 编码，可用 Excel 或 pandas 打开 |
| `mx_stocks_screener_<查询ID>_description.txt` | 数据说明：查询内容、行数、列名说明等 |

## 环境变量

| 变量                        | 说明                    | 默认 |
|---------------------------|-----------------------|------|
| `MX_STOCKS_SCREENER_OUTPUT_DIR` | CSV 与描述文件的输出目录（可选）    | `miaoxiang/mx_stocks_screener` |
| `EM_API_KEY` | 妙想智能选股工具 API 密钥（必备） | 无 |

## 常见问题

**错误：请设置 EM_API_KEY 环境变量**

- 请访问 https://ai.eastmoney.com/mxClaw 获取`API_KEY`。
- 配置`EM_API_KEY`环境变量


**如何指定输出目录？**
```bash
export MX_STOCKS_SCREENER_OUTPUT_DIR="/path/to/output"
python3 {baseDir}/scripts/get_data.py --query "查询内容" --select-type "查询领域"
```