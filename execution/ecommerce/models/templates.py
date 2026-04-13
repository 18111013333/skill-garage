"""合作输出模板 - V4.3.0

统一话术模板，分三层：初次接触、深聊合作、成交跟进
"""

from typing import Dict, List
from dataclasses import dataclass
from string import Template

@dataclass
class ContactScript:
    """联系话术"""
    stage: str              # 阶段
    subject: str            # 主题
    content: str            # 内容
    tips: List[str]         # 注意事项

class ScriptTemplates:
    """话术模板库"""
    
    # 第一层：初次接触
    FIRST_CONTACT = {
        "wechat": Template("""
您好！我是${company}的${name}，专注${category}品类。

看到您在${platform}的表现很棒，特别是${highlight}这块，想跟您聊聊合作机会。

我们目前有${product}，${advantage}，想邀请您帮忙带货。

方便加个微信详聊吗？我的微信：${wechat}
        """),
        
        "dm": Template("""
${greeting}！我是${company}的${name}。

关注您很久了，您的${content_type}做得特别好！

我们有一款${product}，${selling_point}，想邀请您合作。

感兴趣的话可以回复我，或者加微信：${wechat}
        """)
    }
    
    # 第二层：深聊合作
    DEEP_DISCUSSION = {
        "commission": Template("""
感谢您的回复！关于合作细节：

【产品信息】
- 产品：${product}
- 价格：${price}
- 佣金比例：${commission}%
- 预估单场收益：${estimated_income}

【合作方式】
- 样品：${sample_policy}
- 结算：${settlement}
- 售后：${after_sales}

【时间安排】
- 寄样时间：${sample_time}
- 直播时间：${live_time}

您看这个方案可以吗？有什么需要调整的随时说~
        """),
        
        "negotiation": Template("""
理解您的顾虑，我们可以调整：

【调整方案】
- 佣金：${new_commission}%
- 保底：${guaranteed}
- 其他：${other_benefits}

这个方案您觉得怎么样？
        """)
    }
    
    # 第三层：成交跟进
    FOLLOW_UP = {
        "pre_live": Template("""
${name}，直播准备得怎么样了？

【提醒事项】
- 样品收到了吗？
- 脚本需要我帮忙吗？
- 时间确认：${live_time}

有任何问题随时找我！
        """),
        
        "post_live": Template("""
${name}，辛苦了！直播效果很棒！

【数据复盘】
- 观看人数：${viewers}
- 销量：${sales}
- GMV：${gmv}

【结算信息】
- 佣金：${commission}
- 结算时间：${settlement_time}

期待下次合作！
        """),
        
        "reorder": Template("""
${name}，上次合作效果很好！

【新机会】
- 新品：${new_product}
- 优势：${advantage}
- 佣金：${commission}%

有兴趣再合作一次吗？
        """)
    }
    
    @classmethod
    def generate_first_contact(cls, channel: str, **kwargs) -> ContactScript:
        """生成初次接触话术"""
        template = cls.FIRST_CONTACT.get(channel, cls.FIRST_CONTACT["wechat"])
        content = template.safe_substitute(**kwargs)
        
        return ContactScript(
            stage="first_contact",
            subject=f"合作邀请 - {kwargs.get('company', '我们公司')}",
            content=content.strip(),
            tips=[
                "保持简洁，不要太长",
                "突出对方优势",
                "明确表达合作意向",
                "留下联系方式"
            ]
        )
    
    @classmethod
    def generate_deep_discussion(cls, topic: str, **kwargs) -> ContactScript:
        """生成深聊合作话术"""
        template = cls.DEEP_DISCUSSION.get(topic, cls.DEEP_DISCUSSION["commission"])
        content = template.safe_substitute(**kwargs)
        
        return ContactScript(
            stage="deep_discussion",
            subject=f"合作方案 - {kwargs.get('product', '产品')}",
            content=content.strip(),
            tips=[
                "信息要完整准确",
                "佣金要有竞争力",
                "售后要明确"
            ]
        )
    
    @classmethod
    def generate_follow_up(cls, stage: str, **kwargs) -> ContactScript:
        """生成跟进话术"""
        template = cls.FOLLOW_UP.get(stage, cls.FOLLOW_UP["pre_live"])
        content = template.safe_substitute(**kwargs)
        
        return ContactScript(
            stage="follow_up",
            subject="跟进提醒",
            content=content.strip(),
            tips=[
                "及时跟进",
                "保持热情",
                "数据复盘要具体"
            ]
        )
