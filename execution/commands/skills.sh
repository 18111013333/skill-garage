#!/bin/bash
# 技能管理命令

SKILL_REGISTRY="$HOME/.openclaw/workspace/skill_lifecycle/SKILL_REGISTRY.json"

# 查看所有技能
skills_list() {
    echo "📊 已注册技能列表"
    echo "=================="
    cat "$SKILL_REGISTRY" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for cat, info in data['categories'].items():
    print(f\"\n📁 {info['name']} ({cat})\")
    if 'skills' in info:
        for s in info['skills']:
            status = '✅' if s['status'] == 'active' else '💤'
            print(f\"   {status} {s['id']}: {s['name']} v{s['version']}\")
    elif 'count' in info:
        print(f\"   共 {info['count']} 个技能\")
"
}

# 查看技能详情
skills_show() {
    local skill_id=$1
    echo "📊 技能详情: $skill_id"
    echo "=================="
    cat "$SKILL_REGISTRY" | python3 -c "
import json, sys
data = json.load(sys.stdin)
found = False
for cat, info in data['categories'].items():
    if 'skills' in info:
        for s in info['skills']:
            if s['id'] == '$skill_id':
                found = True
                print(f\"名称: {s['name']}\")
                print(f\"状态: {s['status']}\")
                print(f\"版本: {s['version']}\")
                print(f\"创建: {s['created']}\")
                print(f\"执行次数: {s['executions']}\")
                print(f\"成功率: {s['successRate']*100:.1f}%\")
                break
if not found:
    print('未找到技能: $skill_id')
"
}

# 技能总览
skills_overview() {
    echo "📊 技能系统总览"
    echo "=================="
    cat "$SKILL_REGISTRY" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f\"版本: {data['version']}\")
print(f\"总技能数: {data['totalSkills']}\")
print(f\"最后更新: {data['lastUpdated']}\")
print()
print('保证机制:')
for k, v in data['guarantees'].items():
    status = '✅' if v else '❌'
    print(f\"  {status} {k}\")
"
}

# 主命令
case "$1" in
    list) skills_list ;;
    show) skills_show "$2" ;;
    overview) skills_overview ;;
    *) 
        echo "用法: skills <command>"
        echo "命令:"
        echo "  list       - 查看所有技能"
        echo "  show <id>  - 查看技能详情"
        echo "  overview   - 技能总览"
        ;;
esac
