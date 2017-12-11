import logging
from logging import StreamHandler
import os

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
logger.addHandler(StreamHandler())

header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'Cookie': 'JSESSIONID=ABAAABAABEEAAJA2BD85B1839E445E9986FE9D2824B59BB; user_trace_token=20171211150646-a883ac66-2106-421a-9d8b-bd7923fa58b1; _ga=GA1.2.295287109.1512976009; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512976009; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512976009; LGSID=20171211150650-dc1b3342-de41-11e7-9cc5-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F2921958.html; LGRID=20171211150650-dc1b34a6-de41-11e7-9cc5-5254005c3644; LGUID=20171211150650-dc1b3509-de41-11e7-9cc5-5254005c3644; _gid=GA1.2.1910658704.1512976010',
          'Host': 'www.lagou.com',
          'Pragma': 'no-cache',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'}


def main(url):
    resp = requests.get(url, headers=header)
    if resp.status_code == 200:
        body = resp.text
        soup = BeautifulSoup(body, 'lxml')
        _company = list(soup.find('h2', class_='fl').stripped_strings)[0]
        if ' ' in _company:
            _company = _company.split(' ')[0]
        _jd = soup.find('dd', class_='job_bt').stripped_strings
        with open(os.path.join('./detail', _company), 'w', encoding='utf-8') as wf:
            wf.write('\n'.join(_jd))
        logger.debug('done: {}'.format(_company))
    else:
        logger.info('fail: {}'.format(url))


if __name__ == '__main__':
    urls = set()
    with open('./guangzhou.txt', 'r', encoding='utf-8') as rf:
        for index, line in enumerate(rf.readlines(), start=1):
            if index < 0:
                continue
            line = line.strip()
            if line:
                urls.add(line)
    for url in urls:
        main(url)
    with open('done.txt', 'w') as wf:
        wf.write('\n'.join(urls))
