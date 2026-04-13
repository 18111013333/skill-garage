#!/usr/bin/env python3
"""
场景描写生成器
生成生动的场景描写
"""

import json
import sys
from typing import Dict, List, Any
import random

class SceneGenerator:
    """场景描写生成器"""

    # 场景类型
    SCENE_TYPES = {
        'urban': {
            'name': '都市场景',
            'elements': ['高楼', '街道', '人群', '车流', '霓虹灯'],
            'atmosphere': ['喧嚣', '繁忙', '冷漠', '繁华']
        },
        'nature': {
            'name': '自然场景',
            'elements': ['山峦', '河流', '森林', '草原', '天空'],
            'atmosphere': ['宁静', '壮美', '神秘', '清新']
        },
        'indoor': {
            'name': '室内场景',
            'elements': ['家具', '光线', '气味', '声音', '温度'],
            'atmosphere': ['温馨', '压抑', '舒适', '冷清']
        },
        'historical': {
            'name': '历史场景',
            'elements': ['古建筑', '服饰', '器物', '礼仪', '氛围'],
            'atmosphere': ['庄重', '沧桑', '典雅', '神秘']
        },
        'battle': {
            'name': '战斗场景',
            'elements': ['武器', '动作', '声音', '血腥', '紧张'],
            'atmosphere': ['紧张', '激烈', '残酷', '悲壮']
        }
    }

    # 感官描写库
    SENSES = {
        'visual': {
            'name': '视觉',
            'templates': [
                '{主体}在{背景}中{动作}',
                '{光线}照在{物体}上，{效果}',
                '{颜色}的{物体}显得{形容词}'
            ]
        },
        'auditory': {
            'name': '听觉',
            'templates': [
                '{声音}从{方向}传来',
                '{声音}在{空间}中回荡',
                '耳边响起{声音}'
            ]
        },
        'olfactory': {
            'name': '嗅觉',
            'templates': [
                '空气中弥漫着{气味}',
                '{气味}扑面而来',
                '淡淡的{气味}飘过'
            ]
        },
        'tactile': {
            'name': '触觉',
            'templates': [
                '{触感}从{部位}传来',
                '手指触碰到{物体}，{触感}',
                '{温度}的{物体}让人{感受}'
            ]
        }
    }

    # 时间描写
    TIME_DESCRIPTIONS = {
        'dawn': ['晨曦微露', '东方泛白', '第一缕阳光'],
        'morning': ['阳光明媚', '朝气蓬勃', '繁忙的早晨'],
        'noon': ['烈日当空', '正午时分', '阳光直射'],
        'afternoon': ['午后慵懒', '阳光斜照', '时光缓慢'],
        'dusk': ['夕阳西下', '暮色四合', '华灯初上'],
        'night': ['夜幕降临', '星光点点', '寂静的夜'],
        'midnight': ['深夜时分', '万籁俱寂', '月光如水']
    }

    # 天气描写
    WEATHER_DESCRIPTIONS = {
        'sunny': ['晴空万里', '阳光灿烂', '天高云淡'],
        'cloudy': ['阴云密布', '乌云压顶', '天色阴沉'],
        'rainy': ['细雨绵绵', '大雨倾盆', '雨声淅沥'],
        'snowy': ['雪花纷飞', '银装素裹', '白雪皑皑'],
        'windy': ['狂风呼啸', '风声阵阵', '微风拂面'],
        'foggy': ['雾气弥漫', '能见度低', '朦胧不清']
    }

    def __init__(self):
        pass

    def generate_scene(self, scene_type: str = 'urban', mood: str = None) -> Dict[str, Any]:
        """生成场景描写"""
        type_info = self.SCENE_TYPES.get(scene_type, self.SCENE_TYPES['urban'])

        # 生成多感官描写
        descriptions = self._generate_multi_sensory(scene_type, mood)

        # 生成环境描写
        environment = self._generate_environment(scene_type)

        # 生成氛围描写
        atmosphere = self._generate_atmosphere(type_info, mood)

        return {
            'scene_type': scene_type,
            'scene_name': type_info['name'],
            'descriptions': descriptions,
            'environment': environment,
            'atmosphere': atmosphere,
            'full_description': self._combine_descriptions(descriptions, environment, atmosphere),
            'writing_tips': self._get_writing_tips(scene_type)
        }

    def _generate_multi_sensory(self, scene_type: str, mood: str) -> Dict[str, str]:
        """生成多感官描写"""
        descriptions = {}

        # 视觉
        descriptions['visual'] = self._generate_visual(scene_type)

        # 听觉
        descriptions['auditory'] = self._generate_auditory(scene_type)

        # 嗅觉
        descriptions['olfactory'] = self._generate_olfactory(scene_type)

        # 触觉
        descriptions['tactile'] = self._generate_tactile(scene_type, mood)

        return descriptions

    def _generate_visual(self, scene_type: str) -> str:
        """生成视觉描写"""
        visuals = {
            'urban': '高楼林立，玻璃幕墙反射着阳光，街道上人流如织。',
            'nature': '远山如黛，近水含烟，绿树掩映间鸟儿掠过。',
            'indoor': '阳光透过窗帘的缝隙洒进来，在地板上投下斑驳的光影。',
            'historical': '青砖黛瓦，飞檐翘角，古色古香的建筑静静矗立。',
            'battle': '刀光剑影中，尘土飞扬，鲜血染红了地面。'
        }
        return visuals.get(scene_type, visuals['urban'])

    def _generate_auditory(self, scene_type: str) -> str:
        """生成听觉描写"""
        audios = {
            'urban': '车水马龙的喧嚣声、行人的脚步声、远处传来的汽笛声交织在一起。',
            'nature': '鸟鸣声、流水声、风吹树叶的沙沙声，构成自然的交响乐。',
            'indoor': '房间里很安静，只有时钟滴答的声音和远处隐约的人声。',
            'historical': '古钟悠远的回响，马蹄声踏过青石板，远处传来更夫的梆子声。',
            'battle': '刀剑相击的铿锵声、战马的嘶鸣声、士兵的呐喊声震耳欲聋。'
        }
        return audios.get(scene_type, audios['urban'])

    def _generate_olfactory(self, scene_type: str) -> str:
        """生成嗅觉描写"""
        smells = {
            'urban': '空气中混合着汽车尾气、咖啡香和雨后泥土的气息。',
            'nature': '清新的草木香、泥土的芬芳、野花的幽香扑面而来。',
            'indoor': '淡淡的檀香、旧书的纸香、阳光晒过的温暖气息。',
            'historical': '檀香袅袅，茶香四溢，古木的沉香若有若无。',
            'battle': '血腥味、汗臭味、尘土的气息混杂在一起，令人窒息。'
        }
        return smells.get(scene_type, smells['urban'])

    def _generate_tactile(self, scene_type: str, mood: str) -> str:
        """生成触觉描写"""
        touchs = {
            'urban': '微风拂过脸颊，带着一丝凉意，脚下的路面坚硬而冰冷。',
            'nature': '阳光温暖地洒在身上，微风轻柔地抚摸着皮肤。',
            'indoor': '指尖触碰到冰凉的桌面，空气中带着一丝干燥。',
            'historical': '青石板路有些湿滑，丝绸衣料滑过皮肤，细腻而凉爽。',
            'battle': '握着兵器的手心全是汗水，伤口传来阵阵灼痛。'
        }
        return touchs.get(scene_type, touchs['urban'])

    def _generate_environment(self, scene_type: str) -> Dict[str, str]:
        """生成环境描写"""
        time_of_day = random.choice(list(self.TIME_DESCRIPTIONS.keys()))
        weather = random.choice(list(self.WEATHER_DESCRIPTIONS.keys()))

        return {
            'time': random.choice(self.TIME_DESCRIPTIONS[time_of_day]),
            'weather': random.choice(self.WEATHER_DESCRIPTIONS[weather]),
            'lighting': self._get_lighting_description(time_of_day, weather)
        }

    def _get_lighting_description(self, time: str, weather: str) -> str:
        """获取光线描写"""
        if weather in ['rainy', 'cloudy', 'foggy']:
            return '光线昏暗，一切都笼罩在朦胧中'
        elif time in ['dawn', 'dusk']:
            return '柔和的光线，带着温暖的色调'
        elif time in ['noon']:
            return '光线强烈，明暗对比分明'
        elif time in ['night', 'midnight']:
            return '月光和灯光交织，投下斑驳的影子'
        else:
            return '光线明亮，视野清晰'

    def _generate_atmosphere(self, type_info: Dict, mood: str) -> str:
        """生成氛围描写"""
        if mood:
            return f'整个场景弥漫着{mood}的气息'
        else:
            return f'整个场景弥漫着{random.choice(type_info["atmosphere"])}的气息'

    def _combine_descriptions(self, descriptions: Dict, environment: Dict, atmosphere: str) -> str:
        """组合完整描写"""
        parts = [
            f"{environment['time']}，{environment['weather']}。",
            descriptions['visual'],
            descriptions['auditory'],
            descriptions['olfactory'],
            atmosphere + '。'
        ]
        return '\n'.join(parts)

    def _get_writing_tips(self, scene_type: str) -> List[str]:
        """获取写作技巧"""
        tips = {
            'urban': ['注意现代都市的节奏感', '可以加入科技元素', '对比繁华与孤独'],
            'nature': ['调动多种感官', '注意季节特征', '可以借景抒情'],
            'indoor': ['注重细节描写', '通过环境反映人物心理', '注意空间感'],
            'historical': ['注意时代特征', '避免现代词汇', '可以加入历史典故'],
            'battle': ['注意节奏控制', '突出紧张感', '可以加入慢镜头描写']
        }
        return tips.get(scene_type, ['调动多种感官', '注意细节描写', '营造氛围'])

def main():
    """主函数"""
    generator = SceneGenerator()

    if len(sys.argv) < 2:
        # 演示模式
        result = generator.generate_scene('nature', '宁静')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    scene_type = sys.argv[1] if len(sys.argv) > 1 else 'urban'
    mood = sys.argv[2] if len(sys.argv) > 2 else None

    result = generator.generate_scene(scene_type, mood)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
