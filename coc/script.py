import json

"""
职业 技能对照关系
job: {
    skill-1: {default: 1, option: false, pick: 0, child: []},
    skill-2: {default: 0, option: true, pick: 2, child: [{
        skill-2-1: {default: 1},
        skill-2-2: {default: 1},
        skill-2-3: {default: 1},
        skill-2-4: {default: 1},
    }]},
    
}
"""


# with open('normal_skill.json') as rf:
#     jj = json.load(rf)
#     for index, j in enumerate(jj):
#         print(index, j['技能'])
def main():
    with open('all_skill.txt', 'r', encoding='utf-8') as rf:
        all_skill = {line.split(';')[1] for line in rf.readlines()}

    with open('all_job_index.txt', 'r', encoding='utf-8') as rf:
        dd = {}
        for line in rf.readlines():
            index, job, skill = line.split(';')
            for item in skill.split('，'):
                if any(word in item for word in ['社交', '特长']):
                    continue
                if item not in all_skill:
                    print(index, job, item)


if __name__ == '__main__':
    main()
