template = ["小源科技获年度“最佳企业服务商”殊荣,",
            "小源科技获年度“最佳企业服务商”殊荣, 短信公众号将成新流量风口",
            "小源科技获年度“最佳企业服务商”殊荣, 短信公众号将成新流量风",
            "小源科技获年度“最佳企业服务商”殊荣, 推短信公众号或将成为新",
            "小源科技获年度“最佳企业服务商”殊荣, 短信公众号或将成为新风口"]

res = '''\
a 0 [' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 1 [' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 2 ['信', '公', '众', '号'] {1, 2, 3, 4}
a 3 ['信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 4 ['信', '公', '众', '号', '或', '将', '成', '为', '新'] {3, 4}
a 5 ['公', '众', '号'] {1, 2, 3, 4}
a 6 ['公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 7 ['公', '众', '号', '或', '将', '成', '为', '新'] {3, 4}
a 8 ['务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 9 ['务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 10 ['务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 11 ['务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 12 ['号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 13 ['号', '或', '将', '成', '为', '新'] {3, 4}
a 14 ['商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 15 ['商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 16 ['商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 17 ['商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 18 ['将', '成'] {1, 2, 3, 4}
a 19 ['将', '成', '新', '流', '量', '风'] {1, 2}
a 20 ['将', '成', '为', '新'] {3, 4}
a 21 ['小', '源', '科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 22 ['小', '源', '科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 23 ['小', '源', '科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 24 ['小', '源', '科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 25 ['年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 26 ['年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 27 ['年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 28 ['年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 29 ['度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 30 ['度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 31 ['度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 32 ['度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 33 [',', ' '] {1, 2, 3, 4}
a 34 [',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 35 [',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 36 ['成', '新', '流', '量', '风'] {1, 2}
a 37 ['成', '为', '新'] {3, 4}
a 38 ['或', '将', '成', '为', '新'] {3, 4}
a 39 ['技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 40 ['技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 41 ['技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 42 ['技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 43 ['新', '流', '量', '风'] {1, 2}
a 44 ['最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 45 ['最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 46 ['最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 47 ['最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 48 ['服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 49 ['服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 50 ['服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 51 ['服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 52 ['殊', '荣', ','] {0, 1, 2, 3, 4}
a 53 ['殊', '荣', ',', ' '] {1, 2, 3, 4}
a 54 ['殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 55 ['殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 56 ['流', '量', '风'] {1, 2}
a 57 ['源', '科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 58 ['源', '科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 59 ['源', '科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 60 ['源', '科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 61 ['短', '信', '公', '众', '号'] {1, 2, 3, 4}
a 62 ['短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 63 ['短', '信', '公', '众', '号', '或', '将', '成', '为', '新'] {3, 4}
a 64 ['科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 65 ['科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 66 ['科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 67 ['科', '技', '获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 68 ['荣', ','] {0, 1, 2, 3, 4}
a 69 ['荣', ',', ' '] {1, 2, 3, 4}
a 70 ['荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 71 ['荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 72 ['获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 73 ['获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 74 ['获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 75 ['获', '年', '度', '“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 76 ['量', '风'] {1, 2}
a 77 ['风', '口'] {1, 4}
a 78 ['“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 79 ['“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 80 ['“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 81 ['“', '最', '佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 82 ['”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 83 ['”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 84 ['”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 85 ['”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 86 ['业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 87 ['业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 88 ['业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 89 ['业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 90 ['为', '新'] {3, 4}
a 91 ['企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 92 ['企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 93 ['企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 94 ['企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 95 ['众', '号'] {1, 2, 3, 4}
a 96 ['众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}
a 97 ['众', '号', '或', '将', '成', '为', '新'] {3, 4}
a 98 ['佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ','] {0, 1, 2, 3, 4}
a 99 ['佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' '] {1, 2, 3, 4}
a 100 ['佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号'] {1, 2, 4}
a 101 ['佳', '企', '业', '服', '务', '商', '”', '殊', '荣', ',', ' ', '短', '信', '公', '众', '号', '将', '成', '新', '流', '量', '风'] {1, 2}\
'''


if __name__ == '__main__':
    ts = dict()
    for line in res.split('\n'):
        key = line.split('[')[-1].split(']')[0]
        value = line.split('{')[-1].split('}')[0]
        k = v = ''
        exec('k=[' + key + ']')
        exec('v=[' + value + ']')
        ts[''.join(k)] = v

    from suffix_array import AnalyseCommonPart

    aa = AnalyseCommonPart(template)
    res = aa.analyze()
    for k, v in res:
        assert ts[k] == v

