import json

from utls import COL_LIST, logger

FILENAMES = ['data_angela.json', 'data_dk.json', 'data_dog.json']

CAREER_MAP = {
    'Priest': '牧师',
    'Mage': '法师',
    'Druid': '德鲁伊',
    'Rogue': '盗贼',
    'Warlock': '术士',
    'Neutral': '中立',
    'Hunter': '猎人',
    'Paladin': '骑士',
    'Shaman': '萨满',
    'Warrior': '战士',
}


def scrap_core(raw_data):
    try:
        _name = raw_data['cname']
        _rarity = raw_data['rarity']
        _category = raw_data['clazz']
        _career = CAREER_MAP[raw_data['faction']]
        _version = raw_data['seriesName']
        _cost = raw_data['mana']
        _attack = raw_data['attack']
        _health = raw_data['hp']
        _effect = raw_data['rule']
        _kind = raw_data['race']

        return dict(
            zip(COL_LIST, [_name, _rarity, _category, _career, _version, _cost, _attack, _health, _effect, _kind]))
    except KeyError:
        return


def scrap_single(single_file):
    res_lst = []
    for line in single_file:
        for raw_data in line['data']['cards']:
            res = scrap_core(raw_data)
            if res:
                res_lst.append(res)
            else:
                logger.info('fail in {}'.format(raw_data))
    return res_lst


def scrap():
    res = []
    for file in FILENAMES:
        with open(file, 'r', encoding='utf-8') as rf:
            res.extend(scrap_single(json.load(rf)))
    return res


if __name__ == '__main__':
    print(len(scrap()))
