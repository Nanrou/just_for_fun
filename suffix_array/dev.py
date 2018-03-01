def build_suffix_array_by_hash(strings):
    sorted_unique_set = sorted(set([char for char in strings]))
    char_rank_dict = dict()
    for index, char_ in enumerate(sorted_unique_set):
        char_rank_dict[char_] = index
    rank1 = [char_rank_dict[_char] for _char in strings]

    step_length = 1
    length = len(strings)
    while step_length < length:
        rank2 = [(rank1[index], rank1[index + step_length]) for index in range(length - step_length)]
        rank2.extend([(rank1[index], -1) for index in range(length - step_length, length)])
        compound_rank_dict = {compound: index
                              for index, compound in enumerate(sorted(set(rank2)))}

        rank1 = [compound_rank_dict[r] for r in rank2]
        step_length *= 2

    sa = [0 for _ in range(len(rank1))]
    for index in range(len(rank1)):
        sa[rank1[index]] = index

    return sa, rank1


def build_lcp(sa, rank, strings):
    k = 0
    ht = ['-' for _ in range(len(sa))]
    for i in range(len(sa)):
        if rank[i] == 1:
            k = 0
        else:
            if k > 0:
                k -= 1
            j = sa[rank[i] - 1]
            while i + k < len(sa) and j + k < len(sa) and strings[i + k] == strings[j + k]:
                k += 1
        ht[rank[i]] = k
    ht[0] = '-'
    print('build_lcp: ', ht)
    return ht


def cal_height(r, sa):  # 这里假设sa是包括最小标识符的，也就是sa[0] == 0
    n = len(r)
    rank = [0 for _ in range(128)]
    height = [0 for _ in range(128)]
    k = 0
    for i in range(1, n):
        rank[sa[i]] = i
    for i in range(n - 1):  # 在初始化的时候，就将rank末位赋0了
        if k:
            k -= 1
        j = sa[rank[i] - 1]
        while r[i + k] == r[j + k]:
            k += 1
        height[rank[i]] = k
    print('cal_height: ', height)
    return height


def radix_sort(lst, base=10):
    def list_to_buckets(lst, base, iteration):
        buckets = [[] for _ in range(base)]
        for number in lst:
            digit = (number // (base ** iteration)) % base
            buckets[digit].append(number)
        return buckets

    def buckets_to_list(buckets):
        numbers = []
        for bucket in buckets:
            for number in bucket:
                numbers.append(number)
        return numbers

    max_value = max(lst)

    it = 0
    while base ** it <= max_value:
        lst = buckets_to_list(list_to_buckets(lst, base, it))
        it += 1

    return lst


def build_suffix_array_by_doubling(strings):
    m = 128
    r = strings + '$'
    length = len(r)
    sa = [0 for _ in range(length)]
    wa = [0 for _ in range(m)]
    wb = [0 for _ in range(m)]
    wv = [0 for _ in range(m)]
    ws = [0 for _ in range(m)]

    def cmp(st, a, b, l):
        return st[a] == st[b] and st[a + l] == st[b + l]

    x, y = wa, wb

    for i in range(m):
        ws[i] = 0
    for i in range(length):
        x[i] = ord(r[i])
        ws[x[i]] += 1
    for i in range(1, m):  # 最后那个数会是总名次，也就是总排名
        ws[i] += ws[i - 1]
    for i in range(length - 1, -1, -1):
        ws[x[i]] -= 1  # 拿0来讲，sa[0]就会是末尾的下标n
        sa[ws[x[i]]] = i

    j = p = 1
    while p < length:
        p = 0
        for i in range(length - j, length):
            y[p] = i
            p += 1
        for i in range(length):
            if sa[i] >= j:
                y[p] = sa[i] - j
                p += 1
        for i in range(length):
            wv[i] = x[y[i]]
        for i in range(m):
            ws[i] = 0
        for i in range(length):
            ws[wv[i]] += 1
        for i in range(1, m):
            ws[i] += ws[i - 1]
        for i in range(length - 1, -1, -1):
            ws[wv[i]] -= 1
            sa[ws[wv[i]]] = y[i]

        x, y = y, x
        x[sa[0]] = 0
        p = 1
        for i in range(1, length):
            if cmp(y, sa[i - 1], sa[i], j):
                x[sa[i]] = p - 1
            else:
                x[sa[i]] = p
                p += 1
        j <<= 1
        m = p

    print(x)
    return sa


def ttt():
    def cmp(r, a, b, l):
        return r[a] == r[b] and r[a + l] == r[b + l]

    m = 128
    r = 'aabaaaab' + '$'
    length = len(r)
    sa = [0 for _ in range(length)]
    wa = [0 for _ in range(m)]
    wb = [0 for _ in range(m)]
    wv = [0 for _ in range(m)]
    ws = [0 for _ in range(m)]
    x, y = wa, wb

    for i in range(m):
        ws[i] = 0

    print('ws初始化桶: ', ws)
    print('-' * 20)
    for i in range(length):
        x[i] = ord(r[i])
        ws[x[i]] += 1

    print('ws字符串入桶: ', ws)
    print('-' * 20)
    for i in range(1, m):  # ???
        ws[i] += ws[i - 1]

    print('ws与前一项相加: ', ws)
    print('-' * 20)
    for i in range(length - 1, -1, -1):
        print('x: ', x)
        print('sa[--ws[x[{i}]]] = {i}'.format(i=i))
        print('sa[--ws[{x}]] = {i}'.format(x=x[i], i=i))
        print('sa[--{w}] = {i}'.format(w=ws[x[i]], i=i))
        ws[x[i]] -= 1
        print('ws[i]自减后更新为: ', ws)
        sa[ws[x[i]]] = i
        print('sa[{w}] = {i}'.format(w=ws[x[i]], i=i))
        print(sa)
        print('-' * 20, '\n')

    print('after first x: ', x)
    j = p = 1
    while p < length:
        p = 0  # y[]里存放的是按第二关键字排序的子串首字符下标
        for i in range(length - j, length):
            y[p] = i
            p += 1
        for i in range(length):
            if sa[i] >= j:
                y[p] = sa[i] - j
                p += 1
        print('y: ', y)

        for i in range(length):
            wv[i] = x[y[i]]
        print('wv: ', wv)

        for i in range(m):
            ws[i] = 0
        print('ws初始化: ', ws)

        for i in range(length):
            ws[wv[i]] += 1
        print('ws插入项: ', ws)

        for i in range(1, m):
            ws[i] += ws[i - 1]
        print('ws加前一项:', ws)

        for i in range(length - 1, -1, -1):
            ws[wv[i]] -= 1
            sa[ws[wv[i]]] = y[i]
        print('sa: ', sa)

        x, y = y, x
        x[sa[0]] = 0
        p = 1
        for i in range(1, length):
            if cmp(y, sa[i - 1], sa[i], j):  # 去比较两个字符串是否相同
                x[sa[i]] = p - 1
            else:
                x[sa[i]] = p
                p += 1  # p 最终为不同字符串的个数，符合直觉，也就是所有后缀的总数
        print('x: ', x)
        print('-' * 20, j, p)
        j <<= 1
        m = p


def reciprocal_transform(rank):
    sa = [0 for _ in range(len(rank))]
    for i in range(len(rank)):
        sa[rank[i]] = i
    print('before: ', rank)
    print('after: ', sa)
    return sa


if __name__ == '__main__':
    # text_string = '11212'
    text_string = 'aabaaaab'
    # text_string = 'heheda'
    # text_string = 'heheheda'
    # text_string = 'ABRACADABRA!'
    # sa, rank = build_suffix_array_by_hash(text_string)
    # print(sa, rank)
    # build_lcp(sa, rank, text_string)
    # build_suffix_array_by_doubling(text_string)
    # ttt()
    # rank2sa([1, 1, 2, 1, 1, 1, 1, 2])
    # rank2sa([8, 0, 1, 3, 4, 5, 6, 2, 7])
    rank = [4, 6, 8, 1, 2, 3, 5, 7, 0]
    cal_height('aabaaaab$', reciprocal_transform(rank))
    build_lcp(reciprocal_transform(rank), rank, 'aabaaaab$')
