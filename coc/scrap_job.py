import json

"""
{
"职业": "黑帮", "描述": "blabla", "原作向": False, "古典": False, "现代": False,
"细分": True, 
"子类": [
    {"职业": "黑帮老大",
    "本职技能点数": "教育×2+外貌×2",
    "信用范围": "60-95",
    "推荐关系人": "犯罪组织，街头罪犯，警察，地方政府，政治家，法官，工会，律师，同民族的代表。",
    "本职技能": "格斗，射击，法律，聆听，两项社交技能(魅惑、话术、恐吓、说服)，心理学，侦查。",},
    {"职业": "马仔",
    "本职技能点数": "教育×2+敏捷或力量×2",
    "信用范围": "9-20",
    "推荐关系人": "街头罪犯，警察，企业，同民族的代表。",
    "本职技能": "汽车驾驶，格斗，射击，两项社交技能(魅惑、话术、恐吓、说服)，心理学，任意两项其他个人或时代特长。",},
],
}

{
"职业": "绅士、淑女", "描述": "blabla", "原作向": False, "古典": False, "现代": False,
"细分": True, 
"子类": [
    {"职业": "绅士",
    "本职技能点数": "教育×2+外貌×2",
    "信用范围": "40-90",
    "推荐关系人": "上流社会和乡绅，政治家，仆人和农民。",
    "本职技能": "艺术/工艺(任一)，两项社交技能(魅惑、话术、恐吓、说服)，射击(步霰)，历史，外语(任一)，导航，骑术。",},
    {"职业": "淑女",
    "本职技能点数": "教育×2+外貌×2",
    "信用范围": "40-90",
    "推荐关系人": "上流社会和乡绅，政治家，仆人和农民。",
    "本职技能": "艺术/工艺(任一)，两项社交技能(魅惑、话术、恐吓、说服)，射击(步霰)，历史，外语(任一)，导航，骑术。",},
],
}

{
"职业": "研究员", "描述": "blabla", "原作向": False, "古典": False, "现代": False,
"细分": False, 
"子类": [],
"本职技能点数": "教育×4",
"信用范围": "9-30",
"推荐关系人": "学者和其他学术界人士，大型企业，外国政府和个人。",
"本职技能": "历史，图书馆，一项社交技能(魅惑、话术、恐吓、说服)，外语，侦查，任意三项其他学术领域。",
}


"""


def main():
    with open('job.txt', 'r', encoding='utf-8') as rf:
        all_data = []
        start = end = 0
        lines = [line.strip() for line in rf.readlines()]

        for index, line in enumerate(lines):
            if len(line.strip()):
                continue
            else:
                end = index
                all_data.append(detail(lines, start))
                start = end + 1

        all_data.append(detail(lines, start))

    with open('job.json', 'w', encoding='utf-8') as wf:
        json.dump(all_data, wf, ensure_ascii=False)


def detail(lst, start):
    dd = {"职业": lst[start].split('(')[0]}
    dd['原作向'] = True if '原作向' in lst[start] else False
    dd['古典'] = True if '古典' in lst[start] else False
    dd['现代'] = True if '现代' in lst[start] else False
    _first_index = start

    start += 1
    description = []
    while not lst[start].startswith('※') and not lst[start].startswith('本职技能点数'):
        description.append(lst[start])
        start += 1
    dd["描述"] = '\n'.join(description)

    if lst[start].startswith('※') or '、' in lst[_first_index]:
        dd['细分'] = True
        item_list = []
        if lst[start].startswith('※'):
            while lst[start].startswith('※'):
                item = {
                    "职业": lst[start][1:],
                    "本职技能点数": lst[start + 1].split(':', 1)[-1],
                    "信用范围": lst[start + 2].split(':', 1)[-1],
                    "推荐关系人": lst[start + 3].split(':', 1)[-1],
                    "本职技能": lst[start + 4].split(':', 1)[-1],
                }
                item_list.append(item)
                start += 5
            dd['子类'] = item_list
            return dd
        else:
            names = lst[_first_index].split('(')[0].split('、')
            for name in names:
                item = {
                    "职业": name,
                    "本职技能点数": lst[start].split(':', 1)[-1],
                    "信用范围": lst[start + 1].split(':', 1)[-1],
                    "推荐关系人": lst[start + 2].split(':', 1)[-1],
                    "本职技能": lst[start + 3].split(':', 1)[-1],
                }
                item_list.append(item)
            dd['子类'] = item_list
            return dd
    else:
        dd['细分'] = False
        dd["本职技能点数"] = lst[start].split(':', 1)[-1]
        dd["信用范围"] = lst[start + 1].split(':', 1)[-1]
        dd["推荐关系人"] = lst[start + 2].split(':', 1)[-1]
        dd["本职技能"] = lst[start + 3].split(':', 1)[-1]

        return dd


if __name__ == '__main__':
    main()
    with open('job.json', 'r', encoding='utf-8') as rf:
        jj = json.load(rf)
        i = 0
        for j in jj:
            for ik, iv in j.items():
                if ik == '细分' and iv:
                    for ij in j['子类']:
                        for iik, iiv in ij.items():
                            if iik == '本职技能':
                                print(iiv)
                else:
                    if ik == '本职技能':
                        print(iv)

