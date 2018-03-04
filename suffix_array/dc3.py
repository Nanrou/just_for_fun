src_list = []


class Point:
    def __init__(self, idx, val):
        self.idx = idx
        self.val = val
        self.rel_idx = idx


point_list = []
for i, v in enumerate(src_list):
    point_list.append(Point(i, v))
point_orig = point_list[:]


def dc3(in_list):
    b1_b2_list = []
    for i, point in enumerate(in_list):
        if point.val != 0 and i % 3 in (1, 2):
            b1_b2_list.append(point)
            point.val = (point.val, in_list[i + 1].val, in_list[i + 2].val)
        b1_b2_orig = b1_b2_list[:]
        b1_b2_list.sort(key=lambda p: p.val)

        curr_rank = 0
        prev_val = None
        for p in b1_b2_list:
            if prev_val is None:
                curr_rank += 1
                prev_val = p.val
                p.val = curr_rank
                continue
            if p.val != prev_val:
                curr_rank += 1
                prev_val = p.val
            p.val = curr_rank

        if curr_rank != len(b1_b2_list):
            b1_b2_list[:] = [*(obj for i, obj in enumerate(b1_b2_orig) if i % 2 == 0),
                             *(obj for i, obj in enumerate(b1_b2_orig) if i % 2 == 1), ]

            for _ in range(2):
                b1_b2_list.append(Point(-1, 0))
            dc3(b1_b2_list)

    b_0_list = []
    for i, point in enumerate(in_list):
        if point.val != 0 and i % 3 == 0:
            b_0_list.append(point)
            point.val = (point.val, in_list[i + 1].val)
    b_0_list.sort(key=lambda p: p.val)

    for i in range(len(in_list)):
        in_list[i].rel_idx = i

    out_list = []
    while True:
        b_0_head = b_0_list[0]
        b_12_head = b1_b2_list[0]

        def b_0_win():
            out_list.append(b_12_head)
            del b1_b2_list[0]

        def b_12_win():
            out_list.append(b_0_head)
            del b_0_list[0]

        if b_12_head.rel_idx % 3 == 1:
            if src_list[b_0_head.idx] > src_list[b_12_head.idx]:
                b_0_win()
            elif src_list[b_0_head.idx] < src_list[b_12_head.idx]:
                b_12_win()
                # 以上两种为能直接决出胜负的情况

            else:  # 如不能, 一定可以用 b_0 之后的 b_1 和 b_1 之后的 b_2 决出胜负
                if point_orig[b_0_head.idx + 1].val > point_orig[b_12_head.idx + 1].val:
                    b_0_win()
                else:
                    b_12_win()

        else:  # b_0 vs b_2 原理相仿
            if src_list[b_0_head.idx] > src_list[b_12_head.idx]:
                b_0_win()
            elif src_list[b_0_head.idx] < src_list[b_12_head.idx]:
                b_12_win()

            else:
                if src_list[b_0_head.idx + 1] > src_list[b_12_head.idx + 1]:
                    b_0_win()
                elif src_list[b_0_head.idx + 1] < src_list[b_12_head.idx + 1]:
                    b_12_win()

                else:
                    if point_orig[b_0_head.idx + 2].val > point_orig[b_12_head.idx + 2].val:
                        b_0_win()
                    else:
                        b_12_win()

                # 判断是否终结
        if not b_0_list:
            out_list.extend(b1_b2_list)
            break
        elif not b1_b2_list:
            out_list.extend(b_0_list)
            break

    in_list[:] = out_list
    for i in range(len(in_list)):
        in_list[i].val = i
    return in_list


if __name__ == '__main__':
    result = dc3(point_list)
    for i in result:
        print(i.idx)
