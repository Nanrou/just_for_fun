import os
import pickle
from collections import OrderedDict, namedtuple, Counter
import json

import jieba


FILENAMES = ['l_sum', 'z_sum', 'q_sum']
NAME_DICT = {'l_sum': '拉钩', 'z_sum': '智联', 'q_sum': '前程无忧'}
sum_data = namedtuple('sum_data', ['avg_min', 'avg_max', 'mid_salary', 'all_titles', 'all_work_des', 'all_content'])


def myavg(lst):
    return sum(lst) // len(lst)


def count_num_of_job_core(filename):
    try:
        with open(filename, 'rb') as rf:
            pp = pickle.load(rf)
    except FileNotFoundError:
        print('{} not found'.format(filename))
        return 0
    return len(pp)


def count_num_of_job(folder, filename):
    res = OrderedDict()
    for _folder in os.listdir(folder):
        f = os.path.join(folder, _folder)
        t = count_num_of_job_core(os.path.join(f, filename))
        res[_folder] = t
    return res


def count_num_main():  # 统计每个招聘网的岗位数
    res = {}
    for name in FILENAMES:
        _count_res = count_num_of_job('daily_data', name)
        res[name] = _count_res
    with open('count_of_job.json', 'w', encoding='utf-8') as wf:
        wf.write(json.dumps(res))


def filter_job_core(filename):
    res = {}
    with open(filename, 'rb') as rf:
        pp = pickle.load(rf)
        for p in pp:
            _uname = ''.join([p.get('title'), p.get('company')])
            res[_uname] = p
    return res


def analyze_data_core(raw_data):
    min_salary, max_salary = [], []
    title_list = []
    work_des_list = []
    content_list = []
    for _, data in raw_data.items():
        if 'k' in data.get('salary'):
            _min_salary, _max_salary = [int(x.strip().strip('k')) for x in data.get('salary').split('-')]
        elif 'K' in data.get('salary'):
            _min_salary, _max_salary = [int(x.strip().strip('K')) for x in data.get('salary').split('-')]
        elif '万/月' in data.get('salary'):
            _min_salary, _max_salary = [int(float(x.strip()) * 10) for x in data.get('salary').strip('万/月').split('-')]
        elif '元/月' in data.get('salary'):
            _min_salary, _max_salary = [int(x.strip()) // 1000 for x in data.get('salary').strip('元/月').split('-')]
        elif '万/年' in data.get('salary'):
            if '-' in data.get('salary'):
                _min_salary, _max_salary = [int(float(int(x.strip()) // 12) * 10)
                                            for x in data.get('salary').strip('').strip('万/年').split('-')]
            else:
                _min_salary = _max_salary = [int(float(int(data.get('salary').strip('万/年').strip()) // 12) * 10)]

        else:
            _min_salary, _max_salary = 6, 8
        min_salary.append(_min_salary)
        max_salary.append(_max_salary)

        title_list.append(data.get('title'))

        if '职能类别：' in data.get('content'):
            content_list.append(data.get('content').split('职能类别：')[0])
            work_des_list.append(data.get('work_des'))
        elif '工作地址：' in data.get('content'):
            tmp = data.get('content').split('工作地址：')
            _content, _des = tmp[0], tmp[1]
            content_list.append(_content)
            work_des_list.append(_des)
        else:
            content_list.append(data.get('content'))
            work_des_list.append(data.get('work_des'))

    avg_min, avg_max = myavg(min_salary), myavg(max_salary)
    mid_salary = (avg_max + avg_min) // 2

    all_titles = title_list
    all_work_des = work_des_list
    all_words = jieba.lcut(','.join(content_list))
    return sum_data(avg_min, avg_max, mid_salary, all_titles, all_work_des, all_words)


def filter_job_content():  # 汇总，去重每个招聘网的平均薪资，工作地点，关键词
    for name in FILENAMES:
        res = {}
        for _folder in os.listdir('daily_data'):
            filename = os.path.join(os.path.join('daily_data', _folder), name)
            res.update(filter_job_core(filename))
            with open('sum_of_{}.json'.format(name), 'w', encoding='utf-8') as wf:
                wf.write(json.dumps(res, ensure_ascii=False))


def analyze_data():
    for name in FILENAMES:
        with open('sum_of_{}.json'.format(name), 'r', encoding='utf-8') as rf:
            jj = json.load(rf)
            with open('analyzed_of_{}.json'.format(name), 'w', encoding='utf-8') as wf:
                wf.write(json.dumps(analyze_data_core(jj), ensure_ascii=False))


def conclusion():
    for name in FILENAMES:
        with open('analyzed_of_{}.json'.format(name), 'r', encoding='utf-8') as rf:
            jj = json.load(rf)
            datas = sum_data(*jj)
            titles = [x[0] for x in Counter(datas.all_titles).most_common(3)]
            words = [x[0] for x in Counter(datas.all_content).most_common(10)]

            res_txt = '{name}\n平均薪资范围: {min}k ~ {max}k， 平均薪资值: {mid}k\n' \
                      '前三岗位名称: {titles}\n' \
                      '工作描述关键字: {words}\n'.format(name=name, min=datas.avg_min, max=datas.avg_max,
                                                  mid=datas.mid_salary, titles=','.join(titles), words=','.join(words))

            with open('conclusion.txt', 'a', encoding='utf-8') as af:
                af.write(res_txt)


def get_key_words():
    sum_title, sum_word, sum_des = [], [], []
    for name in FILENAMES:
        with open('analyzed_of_{}.json'.format(name), 'r', encoding='utf-8') as rf:
            jj = json.load(rf)
            datas = sum_data(*jj)
            sum_title.extend(datas.all_titles)
            sum_word.extend(datas.all_content)
            sum_des.extend(datas.all_work_des)
    count_of_title = Counter(sum_title).most_common(12)
    count_of_word = Counter(sum_word).most_common(200)
    with open('sum_data.json', 'w', encoding='utf-8') as wf:
        wf.write(json.dumps([count_of_title, count_of_word, sum_des], ensure_ascii=False))


def count_des():
    res = {'市区': [], '唐家': [], '外地': [], '横琴': [], '南湾': []}
    with open('sum_data.json', 'r', encoding='utf-8') as rf:
        jj = json.load(rf)
        for des in jj[-1]:
            if '查看职位地图' in des:
                des.replace('查看职位地图', '')
            if '唐家' in des or '南方软件园' in des:
                res['唐家'].append(des)
            elif '横琴' in des:
                res['横琴'].append(des)
            elif '南湾' in des or '南屏' in des:
                res['南湾'].append(des)
            elif '珠海' in des or '香洲' in des:
                res['市区'].append(des)
            else:
                res['外地'].append(des)
        with open('粗分地址.json', 'w', encoding='utf-8') as wf:
            wf.write(json.dumps(res, ensure_ascii=False, indent=4))


def final_data():
    res = {'avg_min': '8', 'avg_max': '15', 'avg_mid': '11'}
    with open('sum_data.json', 'r', encoding='utf-8') as rf:
        jj = json.load(rf)
        res['titles'] = jj[0]
    with open('shoudong1.json', 'r', encoding='utf-8') as rf:
        jj = json.load(rf)
        res['words'] = jj
    with open('shoudong2.json', 'r', encoding='utf-8') as rf:
        jj = json.load(rf)
        count_of_des = {k: str(len(v)) for k, v in jj.items()}
        res['des'] = count_of_des
    with open('final_data.json', 'w', encoding='utf-8') as wf:
        wf.write(json.dumps(res, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    final_data()
