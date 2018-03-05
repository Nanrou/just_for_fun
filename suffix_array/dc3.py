def dc3(r_list, max_num):
    wa = [0 for _ in range(max_num)]
    wb = [0 for _ in range(max_num)]
    wv = [0 for _ in range(max_num)]

    def radix_sort(r, a, b, n, m):
        ws = [0 for _ in range(m)]
        for i in range(n):
            wv[i] = r[a[i]]

        for i in range(n):
            ws[wv[i]] += 1

        for i in range(1, m):
            ws[i] += ws[i - 1]

        for i in range(n - 1, -1, -1):
            ws[wv[i]] -= 1
            b[ws[wv[i]]] = a[i]

    def f(x, t):
        return x // 3 if x % 3 == 1 else x // 3 + t

    def g(x, t):
        return x * 3 + 1 if x < t else (x - t) * 3 + 2

    def c0(r, a, b):
        return r[a] == r[b] and r[a + 1] == r[b + 1] and r[a + 2] == r[b + 2]

    def c12(k, r, a, b):
        if k == 2:
            return r[a] < r[b] or r[a] == r[b] and c12(1, r, a + 1, b + 1)
        else:
            return r[a] < r[b] or r[a] == r[b] and wv[a + 1] < wv[b + 1]

    length = len(r_list)
    _sa = [0 for _ in range(3 * length)]
    _r = r_list + [0 for _ in range(2 * length)]

    def dc3_core(r, sa, n, m):
        ta = 0
        tb = (n + 1) // 3
        tbc = 0

        rn = r + [0 for _ in range(n)]

        san = sa + [0 for _ in range(n)]

        r[n] = r[n + 1] = 0

        for i in range(n):
            if i % 3:
                wa[tbc] = i
                tbc += 1

        radix_sort(r[2:], wa, wb, tbc, m)
        radix_sort(r[1:], wb, wa, tbc, m)
        radix_sort(r, wa, wb, tbc, m)

        p = 1
        rn[f(wb[0], tb)] = 0
        for i in range(1, tbc):
            if c0(r, wb[i - 1], wb[i]):
                rn[f(wb[i], tb)] = p - 1
            else:
                rn[f(wb[i], tb)] = p
                p += 1

        if p < tbc:
            dc3_core(rn, san, tbc, p)
        else:
            for i in range(tbc):
                san[rn[i]] = i

        for i in range(tbc):
            if san[i] < tb:
                wb[ta] = san[i] * 3
                ta += 1
        if n % 3 == 1:
            wb[ta] = n - 1
            ta += 1

        radix_sort(r, wb, wa, ta, m)

        for i in range(tbc):
            wb[i] = g(san[i], tb)
            wv[wb[i]] = i

        i = j = p = 0
        while i < ta and j < tbc:
            if c12(wb[j] % 3, r, wa[i], wb[j]):
                sa[p] = wa[i]
                # try:
                #     sa[p] = wa[i]
                # except IndexError:
                #     print(p, i)
                #     print('sa: ', len(sa))
                #     print('ta: ', ta)
                i += 1
            else:
                sa[p] = wb[j]
                # try:
                #     sa[p] = wb[j]
                # except IndexError:
                #     print(p, j)
                #     print('sa: ', len(sa))
                #     print('tbc: ', tbc)
                j += 1
            p += 1

        while i < ta:
            sa[p] = wa[i]
            i += 1
            p += 1

        while j < tbc:
            sa[p] = wb[j]
            # try:
            #     sa[p] = wb[j]
            # except IndexError:
            #     print(p, j, tbc)
            #     print('sa: ', len(sa))
            #     print('wb: ', len(wb))
            j += 1
            p += 1

    dc3_core(_r, _sa, length, max_num)
    return _sa


if __name__ == '__main__':
    text_string = 'aabaaaaba'
    tt = [1, 1, 2, 1, 1, 1, 1, 2, 1]
    dc3(tt, 16)
