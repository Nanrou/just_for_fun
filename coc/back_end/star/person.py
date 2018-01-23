"""
假设传入"字典型数据"来初始化PC

"""
from .default_skill_rank import DEFAULT_SKILL_RANK

# 判断难度等级
NORMAL, DIFFICULT, HARD = 1, 0.5, 0.25


class Investigator:
    def __init__(self, data):

        self.name = data['name']

        # 属性
        self.AGE = data['AGE']  # 年龄
        self.STR = data['STR']  # 力量
        self.CON = data['CON']  # 体制
        self.SIZ = data['SIZ']  # 体型
        self.DEX = data['DEX']  # 敏捷
        self.APP = data['APP']  # 外貌
        self.INT = data['INT']  # 智力
        self.POW = data['POW']  # 意志
        self.EDU = data['EDU']  # 教育
        self.LUCK = data['LUCK']  # 幸运
        self.MOV = data['MOV']  # 移动速度
        self.DB = data['DB']  # 伤害加深
        self.BUILD = data['BUILD']  # 体格
        self.MAX_HP = data['MAX_HP']  # 最大生命值
        self.MAX_MP = data['MAX_MP']  # 最大魔法值
        self.MAX_SAN = data['MAX_SAN']  # 最大魔法值
        self.DODGE = data['DODGE']  # 闪避

        # 状态
        self.HP = data['HP']  # 当前HP
        self.MP = data['MP']  # 当前MP
        self.SAN = data['SAN']  # 当前SAN

        self.INSANE = data['INSANE']  # 疯狂
        self.INJURY = data['INJURY']  # 重伤
        self.CLOSE_TO_DEATH = data['CLOSE_TO_DEATH']  # 濒死

        # 技能
        self.SKILLS = data['SKILLS']
        # self.FIRST_LANGUAGE = {data['FIRST_LANGUAGE']: }  # 关于母语的初始化
        # self.CREDIT = data['CREDIT']  # 信用评级

    def degree_of_difficulty(self, attr, rank):
        """
        :param attr: 对应属性/技能
        :param rank: 难度系数
        :return: 对应难度下的成功概率
        """
        _attr = getattr(self, attr) or self._conclude_skill(attr)
        return _attr * rank

    def _conclude_skill(self, attr):  # 该PC没有对应技能的时候，去看默认数值表
        if attr in self.SKILLS:
            return self.SKILLS.get(attr)
        else:
            return DEFAULT_SKILL_RANK.get(attr)


