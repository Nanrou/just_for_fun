

class SuffixArray:
    def __init__(self, r):
        """
        接受 字符串 生成SA数组和Height数组
        :param r: 需要处理的字符串
        """
        # 怎么样找到足够大的m，和足够小的suffix呢
        self.r = r
        self.n = len(r)
        self._rank1 = self._r2rank(r)
        self.m = len(self._rank1)
        self._rank2 = [0 for _ in range(self.m)]
        self._sa = [0 for _ in range(self.m)]
        self._rank = [0 for _ in range(self.m)]
        self._height = [0 for _ in range(self.m)]

        self._build_sa()
        self._build_height()

    @staticmethod
    def _r2rank(r):
        string_rank_mapper = {string: rank
                              for rank, string in enumerate(sorted(set(r)), start=1)}
        rank = [string_rank_mapper[string] for string in r]
        rank.append(0)
        return rank

    def rank2sa(self, rank):
        _sa = [0 for _ in range(self.m)]
        for i in range(self.m):
            _sa[rank[i]] = i
        return _sa

    def get_new_bucket(self):
        return [0 for _ in range(self.m)]

    # def _build_sa_dc3(self):
    #     def dc3(in_list):
    #         b1_b2_list = []
    #         for i, item in enumerate(in_list):
    #
    #
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


if __name__ == '__main__':
    # test_string = 'ABRACADABRA!'
    test_string = 'aabaaaab'
    sa = SuffixArray(test_string)
    print('rank:', sa.rank)
    print('sa: ', sa.sa)
    print('height: ', sa.height)
    # print('lcp of two suffix: ', sa.lcp_of_two_suffix(1, 4))
    # print('longest repeated sub string', sa.longest_repeated_sub_string())
    # print('unique longest repeated sub string', sa.unique_longest_repeated_sub_string())
    # print('k times repeated longest sub string', sa.k_times_repeated_longest_sub_string(2))
    # print('count different sub string', sa.count_different_sub_string())
    sa.print_sa_sub_string()
