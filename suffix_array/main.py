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
    return ht


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
    m = 255
    r = strings
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
    for i in range(1, m):
        ws[i] += ws[i - 1]
    for i in range(length - 1, -1, -1):
        ws[x[i]] -= 1
        sa[ws[x[i]]] = i

    j = p = 1
    while p < length:
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
            ws[ws[i]] += 1
        for i in range(1, m):
            ws[i] += ws[i - 1]
        for i in range(length - 1, -1, -1):
            ws[wv[i]] -= 1
            sa[ws[wv[i]]] = y[i]
        x, y = y, x
        x[sa[0]] = 0
        for i in range(1, length):
            if cmp(y, sa[i - 1], sa[i], j):
                x[sa[i]] = p - 1
            else:
                x[sa[i]] = p
                p += 1
        j <<= 1
        m = p

    print(sa)


if __name__ == '__main__':
    text_string = 'aabaaaab'
    # text_string = 'heheda'
    # text_string = 'heheheda'
    # text_string = 'ABRACADABRA!'
    # sa, rank = build_suffix_array_by_hash(text_string)
    # print(sa, rank)
    # build_lcp(sa, rank, text_string)
    build_suffix_array_by_doubling(text_string)
