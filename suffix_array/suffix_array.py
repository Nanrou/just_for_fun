from bisect import bisect_left
from functools import wraps
import time

from dc3 import dc3 as dc3_build


def time_clock(func, msg='test'):
    @wraps(func)
    def wrapper(*args, **kwargs):
        s = time.time()
        res = func(*args, **kwargs)
        print('-' * 10, '{} 花了 {} 秒'.format(msg, time.time() - s), '-' * 10)
        return res

    return wrapper


class SuffixArray:
    def __init__(self, r, dc3=False, debug=False, already_transformed=False):
        """
        接受 字符串 生成SA数组和Height数组
        :param r: 需要处理的字符串
        """
        # 怎么样找到足够大的m，和足够小的suffix呢
        self.r = r
        self.n = len(r)
        if already_transformed:  # 如果传入的直接就是数字数组的话
            self._rank1 = r + [0]
        else:
            self._rank1 = self._str2rank()
        self.m = len(self._rank1)
        self._rank2 = [0 for _ in range(self.m)]
        self._sa = [0 for _ in range(self.m)]
        self._rank = [0 for _ in range(self.m)]
        self._height = [0 for _ in range(self.m)]
        self.dc3 = dc3

        if debug:
            if dc3:
                time_clock(self._build_sa_dc3, 'DC3')()
            else:
                time_clock(self._build_sa, 'Double')()
        else:
            if dc3:
                self._build_sa_dc3()
            else:
                self._build_sa()

        self._build_height()

    def _str2rank(self):
        string_rank_mapper = {string: rank
                              for rank, string in enumerate(sorted(set(self.r)), start=1)}
        rank = [string_rank_mapper[string] for string in self.r]
        rank.append(0)
        return rank

    def rank2sa(self, rank):
        _sa = [0 for _ in range(self.m)]
        for i in range(self.m):
            _sa[rank[i]] = i
        return _sa

    def get_new_bucket(self):
        return [0 for _ in range(self.m)]

    def _build_sa_dc3(self):
        self._sa = [0] + dc3_build(self._rank1[:-1], self.m)[:self.n]
        # self._sa = dc3_build(self._rank1)
        for i in range(len(self._sa)):
            self._rank[self._sa[i]] = i

    def _build_sa(self):

        def cmp(rank, a, b, l):
            return rank[a] == rank[b] and rank[a + l] == rank[b + l]

        bucket = self.get_new_bucket()
        for i in range(self.n + 1):
            bucket[self._rank1[i]] += 1
        for i in range(1, self.m):
            bucket[i] += bucket[i - 1]
        for i in range(self.n, -1, -1):
            bucket[self._rank1[i]] -= 1
            self._sa[bucket[self._rank1[i]]] = i

        j = p = 1
        m = self.m
        rank2_bucket = self.get_new_bucket()
        while p < self.n + 1:

            p = 0
            for i in range(self.n + 1 - j, self.n + 1):
                self._rank2[p] = i
                p += 1
            for i in range(self.n + 1):
                if self._sa[i] >= j:
                    self._rank2[p] = self._sa[i] - j
                    p += 1

            for i in range(self.n + 1):
                rank2_bucket[i] = self._rank1[self._rank2[i]]
            bucket = self.get_new_bucket()
            for i in range(self.n + 1):
                bucket[rank2_bucket[i]] += 1
            for i in range(1, m):
                bucket[i] += bucket[i - 1]
            for i in range(self.n, -1, -1):
                bucket[rank2_bucket[i]] -= 1
                self._sa[bucket[rank2_bucket[i]]] = self._rank2[i]

            self._rank1, self._rank2 = self._rank2, self._rank1
            self._rank1[self._sa[0]] = 0
            p = 1
            for i in range(1, self.n + 1):
                if cmp(self._rank2, self._sa[i - 1], self._sa[i], j):
                    self._rank1[self._sa[i]] = p - 1
                else:
                    self._rank1[self._sa[i]] = p
                    p += 1

            j <<= 1
            m = p

        self._rank = self._rank1
        self._sa = self.rank2sa(self._rank)

    def _build_height(self):
        k = 0
        for i in range(self.n):
            if self._rank[i] == 1:  # 因为没有真正在字符串后面加一个特殊的标识符，所以需要特殊判断
                self._height[1] = 0
            else:
                if k:
                    k -= 1
                j = self._sa[self._rank[i] - 1]
                while i + k < self.n and j + k < self.n and self.r[i + k] == self.r[j + k]:
                    k += 1
                self._height[self._rank[i]] = k
        self._height[0] = '-'

    @property
    def sa(self):  # 添加的那个标识符会在SA的最前面，所以把第一位去掉
        return self._sa[1:]

    @property
    def rank(self):  # 添加的那个标识符会在字符串的最后，所以把最后一位去掉
        return [i - 1 for i in self._rank[:-1]]  # 因为标识符的排名是0，去掉标识符后，更新整个rank就可以了

    @property
    def height(self):  # 第一项是SA第0项与左越界比较，而且SA第0项是辅助用的标识符，无实际意义，所以去掉，第二项为SA第1项和SA第0项的比较，只会是0，也去掉了
        return self._height[2:]

    def lcp_of_two_suffix(self, a, b):
        """
        求任意两个后缀的最长公共前缀
        :param a: 该后缀起始位置
        :param b: 该后缀起始位置
        :return: 最长公共前缀
        """
        if a == b:
            return self.r[a:]
        a, b = self.rank[a], self.rank[b]
        if a > b:
            a, b = b, a
        length = min(self.height[a: b])
        return self.r[a: a + length]

    def longest_repeated_sub_string(self):
        """
        求出字符串中最长重复子串，可重叠
        :return: 最长重复子串
        """
        index = length = 0
        for i, h in enumerate(self.height):
            if h > length:
                length = h
                index = i
        return self.r[self.sa[index]: self.sa[index] + length]

    def unique_longest_repeated_sub_string(self):
        """
        求出字符串中最长重复子串，不可重叠
        :return: 不重叠的最长重复子串
        """

        def check(k):
            for i in range(len(self.height)):
                if self.height[i] < k:
                    continue
                for j in range(i - 1, -1, -1):
                    if (abs(self.sa[i] - self.sa[j])) >= k:  # 这两个字符的间距大于k，才是不重复
                        return True
            return False

        start, end = 0, self.n
        length = 0
        while start <= end:
            mid = (start + end) // 2
            if check(mid):  # 因为不知道k是多少，所以每次折半去匹配，看有没有能满足的这个长度的
                length = mid
                start = mid + 1
            else:
                end = mid - 1
        if length > 1:
            for index, h in enumerate(self.height):
                if h == length:
                    return self.r[self.sa[index]: self.sa[index] + length]
        else:
            return 0

    def k_times_repeated_longest_sub_string(self, k):

        def check(_mid):
            # _count = 0
            # for i in range(len(self.height)):
            #     if self.height[i] < _mid:
            #         _count = 0
            #         continue
            #
            #     _count += 1
            #     for j in range(i - 1, -1, -1):
            #         if abs(self.sa[j] - self.sa[i]) < _mid:
            #             _count += 1
            #     if _count >= k:
            #         return True
            return False

        start, end = 0, self.n
        length = 0
        while start <= end:
            mid = (start + end) // 2
            if check(mid):
                length = mid
                start = mid + 1
            else:
                end = mid - 1
        if length > 1:
            for index, h in enumerate(self.height):
                if h == length:
                    return self.r[self.sa[index]: self.sa[index] + length]
        else:
            return 'Not Found'

    def count_different_sub_string(self):
        _sum = self.sa[0]
        for i in range(1, self.n):
            _sum += self.n - self.sa[i] + 1 - self.height[i - 1]
        return _sum

    def print_sa_sub_string(self):
        print('\nSA:')
        print('-' * 20)
        for i in self.sa:
            print(self.r[i:])
            break


class AnalyseCommonPart:
    def __init__(self, texts, dc3=False):
        assert isinstance(texts, list)
        self.texts = texts
        self._sa_ins = SuffixArray(self._str2rank(), already_transformed=True, dc3=dc3)
        self._sa = self._sa_ins.sa[len(self.texts):]
        self._height = self._sa_ins.height[len(self.texts):]

        self.place_distribution = self._build_place_distribution()

        self._lcp_string = None
        self._lcp_substring = None

        self._cache = {}

    def _str2rank(self):
        string_rank_mapper = {string: rank
                              for rank, string in enumerate(sorted(set(''.join(self.texts))), start=2)}
        _rank = []
        for item in [[string_rank_mapper[string] for string in text] for text in self.texts]:
            _rank.append(1)
            _rank.extend(item)
        return _rank[1:]

    def _build_place_distribution(self):
        wv = [len(text) for text in self.texts]
        for i in range(1, len(wv)):
            wv[i] += wv[i - 1] + 1
        return [i - 1 for i in wv]

    def get_original_distribution(self, index):
        return bisect_left(self.place_distribution, index)

    def get_original_element(self, index, height=None):  # 这个索引是对应字符串合并后的
        _distribution_index = self.get_original_distribution(index)
        if _distribution_index != 0:
            index -= self.place_distribution[_distribution_index - 1] + 2  # -= 优先级低，也就是先计算完等号右边
        return self.texts[_distribution_index][index: index + height]

    def print_sub_string(self):
        for s in self._sa:
            print('{:0>3}'.format(s), '|||', self.get_original_element(s))

    def analyze(self):
        res = dict()
        # _tt = '$'.join(self.texts)
        for i in range(len(self._height)):
            if self._height[i] > 1:
                # _strings = _tt[self._sa[i + 1]: self._sa[i + 1] + self._height[i]]
                # if '$' in _strings:
                #     _strings = _strings.split('$')[0]

                _strings = self.get_original_element(self._sa[i + 1], self._height[i])

                res.setdefault(_strings, []).extend([self.get_original_distribution(self._sa[i]),
                                                     self.get_original_distribution(self._sa[i + 1])])
                # print('sa_index: {:0>3} || sa: {:0>3} || height: {:0>2} || {}'.format(i, self._sa[i + 1], self._height[i], _tt[self._sa[i + 1]: self._sa[i + 1] + self._height[i]]))

        for _strings, index_list in res.items():
            for index, text in enumerate(self.texts):
                if index not in index_list:
                    if _strings in text:
                        index_list.append(index)
            index_list.sort()

            # self.lcp_string = sorted([[_str, index_list] for _str, index_list in res.items()], key=lambda r: r[0])
            self._lcp_string = res
        # res = list()
        # for i in range(len(self._height)):
        #     if self._height[i] > 1:
        #         _strings = self.get_original_element(self._sa[i + 1], self._height[i])
        #         _index_list = [self.get_original_distribution(self._sa[i]),
        #                        self.get_original_distribution(self._sa[i + 1])]
        #         res.append([_strings, _index_list])
        #
        # for _strings, _index_list in res:
        #     self.get_new_index_of_string(_strings, _index_list)
        # self.lcp_substring = sorted(res, key=lambda r: r[0])

    @property
    def lcp_string(self):
        if 'lcp_string' not in self._cache:
            self._cache['lcp_string'] = sorted(
                [[_str, index_list] for _str, index_list in self._lcp_string.items() if len(_str) > 1],
                key=lambda r: r[0])
        return self._cache['lcp_string']

    def get_new_index_of_string(self, s, i_l):
        for _index, text in enumerate(self.texts):  # 更新 index_list
            if _index not in i_l:
                if s in text:
                    i_l.insert(bisect_left(i_l, _index), _index)
                    # TODO 可以去比较是逐次插入快，还是整体排序快
                    # i_l.append(_index)
        # i_l.sort()

    def lcp_substring_detail_rude(self):
        # res = []
        res = dict()
        sub_distribution = []

        def handler_sub_distribution(sub_distribution_list):
            for index in range(len(sub_distribution_list) - 1):
                # res.append(sub_distribution_list[index])  # 其本身必定就是符合要求的
                res.setdefault(sub_distribution_list[index][0], []).extend(list(sub_distribution_list[index][1]))
                _index_list = list(sub_distribution_list[index][1])
                # 处理两个lcp之间的那些字符串
                for end_place in range(len(sub_distribution_list[index][0]) - 1,
                                       len(sub_distribution_list[index + 1][0]),
                                       -1):
                    _string = sub_distribution_list[index][0][:end_place]
                    self.get_new_index_of_string(_string, _index_list)
                    # res.append([_string, list(_index_list)])  # 注意拷贝
                    res.setdefault(_string, []).extend(list(_index_list))

            # 手动处理分组中最短的那个
            # res.append(sub_distribution_list[-1])
            res.setdefault(sub_distribution_list[-1][0], []).extend(list(sub_distribution_list[-1][1]))
            _index_list = list(sub_distribution_list[-1][1])
            for end_place in range(len(sub_distribution_list[-1][0]) - 1, 1, -1):  # 字符串最短长度为2
                _string = sub_distribution_list[-1][0][:end_place]
                if len(_index_list) != len(self.texts):  # 小优化，一旦全包含了，后面就不需要处理了
                    self.get_new_index_of_string(_string, _index_list)
                # res.append([_string, list(_index_list)])  # 注意拷贝
                res.setdefault(_string, []).extend(list(_index_list))

            return []

        # inverse_index = len(self.lcp_string) - 1
        # tmp_height = [0] + self._height
        # print('height: {}, height->1: {}'.format(len(self._height), len([i for i in self._height if i > 1])))
        # print('len(lcp_string): {}'.format(inverse_index + 1))
        # for height in tmp_height[::-1]:
        #     # print(height)
        #     # print(sub_distribution)
        #     if height > 1:
        #         sub_distribution.append(self.lcp_string[inverse_index])
        #         inverse_index -= 1
        #     elif sub_distribution:  # sub_distribution: [[strings_1, [0, 1]], ...]
        #         start, end = 0, None
        #         for i in range(1, len(sub_distribution)):
        #             if sub_distribution[i][0] not in sub_distribution[i - 1][0]:
        #                 end = i
        #                 handler_sub_distribution(sub_distribution[start: end])
        #                 start = i
        #         sub_distribution = handler_sub_distribution(sub_distribution[start:])
        #     # print(sub_distribution)
        #     # print('*' * 30)

        sub_distribution = list(self.lcp_string)
        start, end = 0, None
        for i in range(1, len(self.lcp_string)):
            if sub_distribution[i][0] not in sub_distribution[i - 1][0]:
                end = i
                handler_sub_distribution(sub_distribution[start: end])
                start = i
        handler_sub_distribution(sub_distribution[start:])

        # res = sorted(list(set(((item[0], tuple(item[1])) for item in res))), key=lambda i: i[0])  # 手动去重
        self._lcp_substring = {k: sorted(set(v)) for k, v in res.items()}

    def lcp_substring_detail_for_test(self):
        res = []
        for string, index_list in self.lcp_string:
            tmp = []
            for end_point in range(len(string), 1, -1):
                ss = string[:end_point]
                self.get_new_index_of_string(ss, index_list)
                tmp.append([ss, index_list])
            res.extend(tmp[::-1])

        res = sorted(set([r[0] for r in res]))

        return res

    @property
    def lcp_substring(self):
        if 'lcp_substring' not in self._cache:
            self._cache['lcp_substring'] = sorted(
                [[_str, index_list] for _str, index_list in self._lcp_substring.items()], key=lambda r: r[0])
        return self._cache['lcp_substring']


if __name__ == '__main__':
    # test_string = 'ABRACADABRA!'
    # test_string = 'aabaaaab'
    # with open('test.txt', 'r') as rf:
    #     test_string = rf.read()
    # sa = SuffixArray(test_string, dc3=True, debug=True)
    # s1 = sa
    # sa = SuffixArray(test_string, debug=True)
    # print('rank:', s1.rank == sa.rank)
    # print('sa: ', s1.sa == sa.sa, len(s1.sa), len(sa.sa))
    # print('height: ', s1.height == sa.height)

    # print('lcp of two suffix: ', sa.lcp_of_two_suffix(1, 4))
    # print('longest repeated sub string', sa.longest_repeated_sub_string())
    # print('unique longest repeated sub string', sa.unique_longest_repeated_sub_string())
    # print('k times repeated longest sub string', sa.k_times_repeated_longest_sub_string(2))
    # print('count different sub string', sa.count_different_sub_string())
    # sa.print_sa_sub_string()

    tt = [
        "小源科技获年度“最佳企业服务商”殊荣,",
        "小源科技获年度“最佳企业服务商”殊荣, 短信公众号将成新流量风口",
        "小源科技获年度“最佳企业服务商”殊荣, 短信公众号将成新流量风",
        "小源科技获年度“最佳企业服务商”殊荣, 推短信公众号或将成为新",
        "小源科技获年度“最佳企业服务商”殊荣, 短信公众号或将成为新风口",
    ]

    # aa = AnalyseCommonPart(tt * 3)
    # aa.analyze()
    # print(len(aa.lcp_string))
    # for l in aa.lcp_string:
    #     print(l)
    # print('-' * 30)
    # aa.lcp_substring_detail_rude()
    # for a in aa.lcp_substring:
    #     print(a)
    # print(len(aa.lcp_substring))
    # rr = aa.lcp_substring_detail_for_test()
    # print(len(rr))

    # dd = {r: 0 for r in rr}
    #
    # for s, _ in aa.lcp_substring:
    #     try:
    #         dd[s] += 1
    #     except KeyError:
    #         print('miss substring: ', s)
    #
    # for k, v in dd.items():
    #     if v != 1:
    #         print(k, v)

    for _ in range(5):
        aa = AnalyseCommonPart(tt * 200)
        time_clock(aa.analyze, 'double 构造')()
        time_clock(aa.lcp_substring_detail_rude, 'substring')()

        aa = AnalyseCommonPart(tt * 200, dc3=True)
        time_clock(aa.analyze, 'dc3 构造')()
        time_clock(aa.lcp_substring_detail_rude, 'substring')()

        print('-' * 20)
