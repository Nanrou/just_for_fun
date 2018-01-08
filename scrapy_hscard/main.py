import json

from utls import logger
from scrapy_from_yingdi import scrap as scrap_yingdi
from scrapy_from_nga import scrap as scrap_nga


def main():
    _tmp = scrap_nga()
    _tmp.extend(scrap_yingdi())
    with open('data_version_1.json', 'w', encoding='utf-8') as wf:
        json.dump(_tmp, wf, ensure_ascii=False)
    logger.info('共导入 {} 条数据'.format(len(_tmp)))


# TODO 将仆从改回随从，数据一致性

if __name__ == '__main__':
    main()
