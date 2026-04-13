# Huawei-Drive 命令快速参考

## 查询命令

### 查询可用空间

```bash
huawei_drive.py --command query --id available_space
```

> 该命令返回int类型，表示云空间剩余可用空间

### 查询文件是否存在

```bash
huawei_drive.py --command query --file_name <file_name>
```

> 该命令返回0表示云盘中存在同名文件，返回1表示不存在同名文件

### 查询文件夹`小艺claw`是否存在

```bash
huawei_drive.py --command query_folder --file_name 小艺claw
```

## 文件上传命令

### 文件覆盖上传

```bash
huawei_drive.py --command upload --mode overwrite --path <file_path>
```

> 该命令在`/root/小艺claw`目录下上传文件，若文件已存在则覆盖原有文件

### 文件重命名上传

```bash
huawei_drive.py --command upload --mode rename --path <file_path>
```

> 该命令在`/root/小艺claw`目录下上传文件，若文件已存在则重命名上传文件

## 文件夹命令

### 创建 小艺claw 文件夹

```bash
huawei_drive.py --command create --folder_name 小艺claw
```

> 该命令在云盘根路径下创建`小艺claw`文件夹