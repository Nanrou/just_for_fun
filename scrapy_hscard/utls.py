import logging

"""
数据初步设定为: 
[卡牌名字， 稀有度， 分类， 从属， 版本， 法力值， 攻击力， 生命值， 效果， 种族]
example:
['穆克拉', '传说', '随从', '中立', '专家级', '3', '5', '5', '战吼：使你的对手获得两个香蕉。', '野兽']
['黄铜指虎', '史诗', '武器', '战士', '龙争虎斗加基森', '4', '2', '3', '在你的英雄攻击后，使你手牌中的一个随机随从牌获得+1/+1。', '']
['影袭', '基本', '法术', '盗贼', '基本级', '1', '', '', '对敌方英雄造成3点伤害。', '']
"""

logger = logging.getLogger('hs_logger')

ch = logging.StreamHandler()
_date_format = '%H:%M:%S'
_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', _date_format)
ch.setFormatter(_formatter)

logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

COL_LIST = ['name', 'rarity', 'category', 'career', 'version', 'cost', 'attack', 'health', 'effect', 'kind']

