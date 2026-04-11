#!/usr/bin/env python3
"""
人物关系图谱工具
生成和管理故事中的人物关系网络
"""

import json
import sys
from typing import Dict, List, Any, Set
from collections import defaultdict

class RelationshipMapper:
    """人物关系图谱"""

    # 关系类型
    RELATIONSHIP_TYPES = {
        'family': {
            'name': '家庭关系',
            'subtypes': ['父母', '子女', '兄弟姐妹', '配偶', '亲戚']
        },
        'friendship': {
            'name': '友情关系',
            'subtypes': ['挚友', '好友', '普通朋友', '酒肉朋友']
        },
        'romance': {
            'name': '爱情关系',
            'subtypes': ['恋人', '前任', '暗恋', '暧昧', '情敌']
        },
        'rivalry': {
            'name': '敌对关系',
            'subtypes': ['死敌', '对手', '竞争者', '仇人']
        },
        'professional': {
            'name': '职业关系',
            'subtypes': ['上司', '下属', '同事', '合作伙伴', '竞争对手']
        },
        'mentor': {
            'name': '师徒关系',
            'subtypes': ['师父', '徒弟', '师兄妹', '同门']
        }
    }

    # 关系强度
    STRENGTH_LEVELS = {
        'strong': {'name': '强关系', 'weight': 3},
        'medium': {'name': '中等关系', 'weight': 2},
        'weak': {'name': '弱关系', 'weight': 1}
    }

    # 关系状态
    RELATIONSHIP_STATUS = {
        'active': '当前关系',
        'past': '过去关系',
        'potential': '潜在关系',
        'broken': '破裂关系'
    }

    def __init__(self):
        self.characters = {}
        self.relationships = []

    def add_character(self, character: Dict[str, Any]) -> None:
        """添加角色"""
        self.characters[character['id']] = character

    def add_relationship(self, char1_id: str, char2_id: str,
                        rel_type: str, subtype: str,
                        strength: str = 'medium',
                        status: str = 'active',
                        description: str = '') -> None:
        """添加关系"""
        relationship = {
            'char1': char1_id,
            'char2': char2_id,
            'type': rel_type,
            'subtype': subtype,
            'type_name': self.RELATIONSHIP_TYPES[rel_type]['name'],
            'strength': strength,
            'strength_name': self.STRENGTH_LEVELS[strength]['name'],
            'status': status,
            'status_name': self.RELATIONSHIP_STATUS[status],
            'description': description
        }
        self.relationships.append(relationship)

    def get_character_relationships(self, char_id: str) -> List[Dict[str, Any]]:
        """获取角色的所有关系"""
        relations = []
        for rel in self.relationships:
            if rel['char1'] == char_id or rel['char2'] == char_id:
                other_id = rel['char2'] if rel['char1'] == char_id else rel['char1']
                other_char = self.characters.get(other_id, {'name': other_id})
                relations.append({
                    'character': other_char,
                    'relationship': rel
                })
        return relations

    def get_relationship_network(self) -> Dict[str, Any]:
        """获取关系网络"""
        nodes = []
        edges = []

        # 构建节点
        for char_id, char in self.characters.items():
            nodes.append({
                'id': char_id,
                'name': char.get('name', char_id),
                'role': char.get('role', 'unknown')
            })

        # 构建边
        for rel in self.relationships:
            edges.append({
                'source': rel['char1'],
                'target': rel['char2'],
                'type': rel['type'],
                'label': rel['subtype'],
                'strength': rel['strength']
            })

        return {
            'nodes': nodes,
            'edges': edges,
            'statistics': self._calculate_statistics()
        }

    def _calculate_statistics(self) -> Dict[str, Any]:
        """计算网络统计"""
        type_counts = defaultdict(int)
        for rel in self.relationships:
            type_counts[rel['type']] += 1

        return {
            'total_characters': len(self.characters),
            'total_relationships': len(self.relationships),
            'relationship_types': dict(type_counts),
            'avg_relationships_per_char': len(self.relationships) * 2 / len(self.characters) if self.characters else 0
        }

    def find_path(self, char1_id: str, char2_id: str) -> List[List[str]]:
        """查找两个角色之间的关系路径"""
        # BFS查找所有路径
        paths = []
        queue = [(char1_id, [char1_id])]
        visited = set()

        while queue:
            current, path = queue.pop(0)

            if current == char2_id:
                paths.append(path)
                continue

            if len(path) > 5:  # 限制路径长度
                continue

            for rel in self.relationships:
                if rel['char1'] == current and rel['char2'] not in path:
                    queue.append((rel['char2'], path + [rel['char2']]))
                elif rel['char2'] == current and rel['char1'] not in path:
                    queue.append((rel['char1'], path + [rel['char1']]))

        return paths

    def analyze_conflicts(self) -> List[Dict[str, Any]]:
        """分析潜在冲突点"""
        conflicts = []

        for rel in self.relationships:
            if rel['type'] in ['rivalry', 'romance']:
                conflicts.append({
                    'type': '直接冲突',
                    'characters': [rel['char1'], rel['char2']],
                    'reason': f"{rel['type_name']}: {rel['subtype']}",
                    'intensity': rel['strength']
                })

        # 检查三角关系
        char_relations = defaultdict(set)
        for rel in self.relationships:
            char_relations[rel['char1']].add(rel['char2'])
            char_relations[rel['char2']].add(rel['char1'])

        for char_id, related in char_relations.items():
            for other in related:
                common = related & char_relations[other]
                for third in common:
                    if third != char_id and third != other:
                        conflicts.append({
                            'type': '三角关系',
                            'characters': [char_id, other, third],
                            'reason': '存在共同关联人物',
                            'intensity': 'medium'
                        })

        return conflicts

    def generate_mermaid_diagram(self) -> str:
        """生成Mermaid关系图"""
        lines = ['graph TD']

        # 添加节点
        for char_id, char in self.characters.items():
            name = char.get('name', char_id)
            lines.append(f'    {char_id}["{name}"]')

        # 添加关系
        for rel in self.relationships:
            char1_name = self.characters.get(rel['char1'], {}).get('name', rel['char1'])
            char2_name = self.characters.get(rel['char2'], {}).get('name', rel['char2'])

            if rel['type'] == 'family':
                style = '---'
            elif rel['type'] == 'romance':
                style = '-..-'
            elif rel['type'] == 'rivalry':
                style = '--x'
            else:
                style = '---'

            lines.append(f'    {rel["char1"]} {style}|{rel["subtype"]}| {rel["char2"]}')

        return '\n'.join(lines)

def create_demo_network() -> RelationshipMapper:
    """创建演示网络"""
    mapper = RelationshipMapper()

    # 添加角色
    mapper.add_character({'id': 'protagonist', 'name': '主角', 'role': 'protagonist'})
    mapper.add_character({'id': 'antagonist', 'name': '反派', 'role': 'antagonist'})
    mapper.add_character({'id': 'love_interest', 'name': '女主', 'role': 'love_interest'})
    mapper.add_character({'id': 'best_friend', 'name': '挚友', 'role': 'supporting'})
    mapper.add_character({'id': 'mentor', 'name': '师父', 'role': 'mentor'})

    # 添加关系
    mapper.add_relationship('protagonist', 'antagonist', 'rivalry', '死敌', 'strong', 'active', '宿命之敌')
    mapper.add_relationship('protagonist', 'love_interest', 'romance', '恋人', 'strong', 'active', '相爱')
    mapper.add_relationship('protagonist', 'best_friend', 'friendship', '挚友', 'strong', 'active', '生死之交')
    mapper.add_relationship('protagonist', 'mentor', 'mentor', '徒弟', 'strong', 'active', '师徒情深')
    mapper.add_relationship('antagonist', 'love_interest', 'romance', '前任', 'medium', 'past', '旧情')
    mapper.add_relationship('mentor', 'antagonist', 'mentor', '师兄', 'medium', 'past', '同门')

    return mapper

def main():
    """主函数"""
    mapper = create_demo_network()

    if len(sys.argv) < 2:
        # 演示模式
        result = mapper.get_relationship_network()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    command = sys.argv[1]

    if command == 'network':
        result = mapper.get_relationship_network()
    elif command == 'conflicts':
        result = mapper.analyze_conflicts()
    elif command == 'path':
        char1 = sys.argv[2] if len(sys.argv) > 2 else 'protagonist'
        char2 = sys.argv[3] if len(sys.argv) > 3 else 'antagonist'
        result = {'paths': mapper.find_path(char1, char2)}
    elif command == 'mermaid':
        result = {'diagram': mapper.generate_mermaid_diagram()}
    else:
        result = mapper.get_relationship_network()

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
