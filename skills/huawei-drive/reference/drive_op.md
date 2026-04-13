# 云盘操作

描述如何查询云盘信息，支持查询云空间总大小和支持云盘上传的剩余空间大小。

## 查询云盘大小

查询云盘的空间大小信息，并返回 Markdown 信息描述。

### 执行步骤

1. 用户提及查询云盘信息，查询云盘空间大小时执行
2. 调用 `huawei_drive.py` 指定命令`query`进行查询

### 输出格式
```
云盘剩余空间大小为 500.12 MB。
```
> 调用命令查询到的大小单位为Byte，输出格式按空间大小转化为按TB/GB/MB/KB为单位。

### CLI 命令示例

```bash
# 查询云盘剩余可用空间
python huawei_drive.py --command query --id available_space
```