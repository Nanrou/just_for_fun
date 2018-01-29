import json

"""
{
    "技能": "会计",
    "初始值": 5,
    "非常规": False, 
    "现代": False,
    "描述": "使你理解会计工作的流程以及一个企业或者个人的金融职务。通过检查账簿，你可以发现做假账的员工，对资金的偷偷挪用，对行贿或者敲诈的款项支付，以及经济状况是否比表面陈述的更好或者更差。通过仔细检查旧账户，你可以了解过去的资金的得与失（谷物，奴隶贸易，威士忌酒的运营等）以及这些资金是付给了谁以及为了什么款项而支付。"
    "辅助信息": "",
}

"""


def main():
    with open('skill.txt', 'r', encoding='utf-8') as rf:
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

        # all_data.append(detail(lines, start))

    with open('normal_skill.json', 'w', encoding='utf-8') as wf:
        json.dump(all_data, wf, ensure_ascii=False)


def detail(lst, start):
    dd = {"技能": lst[start].split('（')[0]}
    dd["非常规"] = True if "非常规" in lst[start] else False
    dd["现代"] = True if "现代" in lst[start] else False
    dd["初始值"] = lst[start].split('（')[-1].split('%')[0]

    start += 1
    description = []
    while not lst[start].startswith('对抗技能/难度等级'):
        description.append(lst[start])
        start += 1
    dd["描述"] = '\n'.join(description)

    assist_text = []
    while len(lst[start].strip()):
        assist_text.append(lst[start])
        start += 1
        if start > 496:
            break
    dd["辅助信息"] = '\n'.join(assist_text)
    return dd


if __name__ == '__main__':
    main()

