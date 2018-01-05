import json

from bs4 import BeautifulSoup

from utls import COL_LIST, logger

CLASS_MAP = {
    '5': '传说',
    '4': '史诗',
    '3': '稀有',
    '2': '普通',
    '1': '基本',
}


def get_text(html_data):
    if isinstance(html_data, str) and html_data.startswith('<'):
        return BeautifulSoup(html_data, 'lxml').text
    else:
        return html_data


def scrap_core(raw_data):
    try:
        raw_data = list(map(get_text, [data for data in raw_data]))

        _name = raw_data[1][1:]
        _rarity = CLASS_MAP[raw_data[1][0]]
        _category = raw_data[2]
        _career = raw_data[3]
        _version = raw_data[7]
        _cost = raw_data[4]
        _attack = raw_data[5]
        _health = raw_data[6]
        _effect = raw_data[10]
        _kind = raw_data[9]
        return dict(
            zip(COL_LIST, [_name, _rarity, _category, _career, _version, _cost, _attack, _health, _effect, _kind]))
    except IndexError or KeyError:
        return


def scrap():
    with open('data1.json', 'r', encoding='utf-8') as rf:
        res_lst = []
        jj = json.load(rf)
        for j in jj:
            res = scrap_core(j)
            if res:
                res_lst.append(res)
            else:
                logger.info('fail in {}'.format(j))
        return res_lst


if __name__ == '__main__':
    print(len(scrap()))
