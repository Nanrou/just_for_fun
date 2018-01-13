from random import choice, random
import pandas as pd

RARITY = ['普通', '稀有', '史诗', '传说']
TOTAL_DUST = 514 * 2 * 40 + 374 * 2 * 100 + 231 * 2 * 400 + 206 * 1600
RAW_DUST = {'普通': 40, '稀有': 100, '史诗': 400, '传说': 1600}
RESOLVE_DUST = {'普通': 5, '稀有': 20, '史诗': 100, '传说': 400}
NORMAL_CARD = ['普通', '稀有', '史诗']
LEGEND_CARD = ['传说']

CHANCE_COMMON = 0.713
CHANCE_RARE = 0.231
CHANCE_EPIC = 0.043
CHANCE_LEGEND = 0.013
CHANCE_MAPPER = {k: v for k, v in zip(RARITY, [CHANCE_COMMON, CHANCE_RARE, CHANCE_EPIC, CHANCE_LEGEND])}


class MockFetch:
    def __init__(self, data_file):
        """
        初始化

        my_cards: {'传说': {'黑骑士': 0, '死亡之翼': 1, ...}, ...}
        card_pool: {'传说': ['黑骑士', '死亡之翼', ...], ...}
        duplicate_legend: 作为原传说卡池的副本，抽一减一
        count: 开的卡包计数
        superfluous_dust: 分解多余卡所得到的总尘数
        already_have_dust: 已有卡对应的总尘数

        整体逻辑为：
            mock(循环开包) -> fetch(从卡池抽卡) -> calculate(更新已有卡库) -> compute_dust(分解卡，计算尘)
        """
        self.my_cards = {k: {} for k in RARITY}
        self.card_pool = {k: [] for k in RARITY}
        self.init_card_pool(data_file)
        self.duplicate_legend = set(self.card_pool['传说'])

        self.count = 0
        self.superfluous_dust = 0
        self.already_have_dust = 0

    def init_card_pool(self, data_file):  # 初始化字典
        all_data = pd.read_json(data_file, encoding='utf-8')
        for row in all_data.iterrows():
            _rarity, _name = row[1]['rarity'], row[1]['name']
            if _rarity in RARITY:
                self.card_pool[_rarity].append(_name)
                self.my_cards[_rarity][_name] = 0

    def finish(self):  # 结束的判断，就是分解得到的尘大于未获得卡的总尘数
        # print('多余的尘：{}，已有卡价值{}尘'.format(self.superfluous_dust, self.already_have_dust))
        return self.superfluous_dust > TOTAL_DUST - self.already_have_dust

    def fetch(self, rarity):  # 随机从目标卡池抽卡，对传说卡池有特殊判断
        if rarity == '传说' and len(self.duplicate_legend):
            _card = choice(self.duplicate_legend)
            self.duplicate_legend.remove(_card)
        else:
            _card = choice(self.card_pool[rarity])
        return _card

    def calculate(self, rarity, card):  # 对已有卡数量进行更新
        self.my_cards[rarity][card] += 1
        self.compute_dust(rarity, card)

    def compute_dust(self, rarity, card):  # 计算尘
        _upper_limit = 2 if rarity in NORMAL_CARD else 1

        if self.my_cards[rarity][card] > _upper_limit:  # 卡数多余上限直接分解掉
            self.superfluous_dust += RESOLVE_DUST[rarity]
            self.my_cards[rarity][card] -= 1
        else:
            self.already_have_dust += RAW_DUST[rarity]

    def mock(self):
        """
        以抽5次卡为一次小循环，用一个flag变量做为标记，前4次没有蓝卡或以上，则第5次调整概率，让它一定落在蓝卡或以上。

        """
        while not self.finish():
            _flag = False
            for _ in range(4):
                _chance = random()
                for rarity in RARITY[1::-1]:  # 如果有非白卡，则设flag为True
                    if _chance < CHANCE_MAPPER[rarity]:
                        _card = self.fetch(rarity)
                        self.calculate(rarity, _card)
                        _flag = True
                        break
                else:
                    _card = choice(self.card_pool['普通'])
                    self.calculate('普通', _card)

            _last_chance = random()
            if _flag:
                pass
            else:
                while _last_chance > CHANCE_RARE:  # 让概率落在非白卡区间
                    _last_chance = random()
            for rarity in RARITY[::-1]:
                if _last_chance < CHANCE_MAPPER[rarity]:
                    _card = choice(self.card_pool[rarity])
                    self.calculate(rarity, _card)

            self.count += 1


if __name__ == '__main__':
    res = []
    for i in range(1, 101):
        mm = MockFetch('data_version_2.json')
        mm.mock()
        res.append(mm.count)
        print('完成度{:0>3}/100'.format(i))
    print('平均值：{}， 最大值：{}， 最小值：{}'.format(sum(res) // 100, max(res), min(res)))
