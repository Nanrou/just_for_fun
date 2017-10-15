def bag_10(N, V, cost_list, worth_list):
    if len(cost_list) == N:
        cost_list = list(cost_list)
        cost_list.insert(0, 0)
    if len(worth_list) == N:
        worth_list = list(worth_list)
        worth_list.insert(0, 0)
        
    res = [[ 0 for _ in range(V+1)] for _ in range(N+1)]
    for i in range(1, N+1):
        for j in range(cost_list[i], V+1):
            res[i][j] = max(res[i-1][j], res[i-1][j-cost_list[i]] + worth_list[i])
            # j - cost_list[i] == 0 也是可以的，因为这时是0
    return res
    
    
def bag_10_one(N, V, cost_list, worth_list):
    if len(cost_list) == N:
        cost_list = list(cost_list)
        cost_list.insert(0, 0)
    if len(worth_list) == N:
        worth_list = list(worth_list)
        worth_list.insert(0, 0)
        
    res = [ 0 for _ in range(V+1)]
    for i in range(1, N+1):
        for j in range(V, cost_list[i]-1, -1):  # 倒序的目的是保证第i次循环中的F[i,v]是由F[i-1,v-Ci]递推而来的。保证每件物品只选一次。
            if j < cost_list[i]:                # 且如果是正序，用的就是新值了
                res[j] = res[j]
            else:
                res[j] = max(res[j], res[j-cost_list[i]] + worth_list[i])
                
    return res

# 时间复杂度上仍然是O(N*V)，但是空间可以降维，在二维数组表达中，每次是与之前一行的同位比较，在一维数组的表达中，每次是与同位比较，若有变化则直接刷新同位。


def bag_10_filled(N, V, cost_list, worth_list):
    if len(cost_list) == N:
        cost_list = list(cost_list)
        cost_list.insert(0, 0)
    if len(worth_list) == N:
        worth_list = list(worth_list)
        worth_list.insert(0, 0)
        
    res = [[ float('-inf') for _ in range(V+1)] for _ in range(N+1)]
    for j in range(N+1):
        res[j][0] = 0
        
    for i in range(1, N+1):
        for j in range(1, V+1):
            if j < cost_list[i]:
                res[i][j] = res[i-1][j]
            else:
                res[i][j] = max(res[i-1][j], res[i-1][j-cost_list[i]] + worth_list[i])
                
    return res  

    
def bag_10_one_filled(N, V, cost_list, worth_list):
    if len(cost_list) == N:
        cost_list = list(cost_list)
        cost_list.insert(0, 0)
    if len(worth_list) == N:
        worth_list = list(worth_list)
        worth_list.insert(0, 0)
        
    res = [ float('-inf') for _ in range(V+1)]
    res[0] = 0
    for i in range(1, N+1):
        for j in range(V, 0, -1):
            if j < cost_list[i]:
                res[j] = res[j]
            else:
                res[j] = max(res[j], res[j-cost_list[i]] + worth_list[i])
                
    return res  

    
def knap_rec(res, cost_list, n):  # 逆向求出是哪几个数组成的res
    if res == 0: 
        return True
    if res < 0 or (res > 0 and n < 1):
        return False
    if knap_rec(res - cost_list[n-1], cost_list, n-1):
        print('Item' + str(n) + ':', cost_list[n-1])
        return True
    if knap_rec(res, cost_list, n-1):
        return True
    else: return False
    
def reverse_trace(res, N, V):
    i = N
    j = V
    while i > 0 and j > 0:
        if res[i][j] != res[i-1][j]:    # 选了第i个物品;与上一行的正上方比较，若相等则说明没有用第i项
            print("第%s个物品，空间：%s，价值：%s" % (i,c[i],v[i]))
            j -= c[i]  # 用了第i项的话，则要去到剩余空间那一列开始比较
        # 考察前一个物品，无论如何，一个物品最多只会被用一次，所以递减去判断
        i -= 1
    

def bag_10_rec(i, j):  # i是第i件物品，j是剩余空间
    if i == -1:
        return 0
    if j < cost_list[i]:
        r = bag_10_rec(i-1, j)       
    else:
        r = max(bag_10_rec(i-1, j), bag_10_rec(i-1, j-cost_list[i]) + worth_list[i])
    return r
    
# 给一个整数的集合，要把它分成两个集合，要两个集合的数的和最接近。
# 理解成从一个集合里面取出元素，也就是一共有N个元素，然后这里的元素的费用和价值是一致的，其背包容量V不应该超过集合的和的二分之一。
# 所以最后转换成，在不超过背包容量V（集合的和的二分之一）这个前提下，求取出部分的最大值（最高价值），也就是其数字本身的和。
# 给定一集和L，则N是len(L)，HALF=sum(L)/2

def bag_10_variant(L):
    N = len(L)
    HALF = sum(L)//2
    if len(L) == N:
        L = list(L)
        L.insert(0, 0)
        
    res = [0 for _ in range(HALF+1)]
    for i in range(1, N+1):
        for j in range(HALF, L[i]-1, -1):
            res[j] = max(res[j], res[j-L[i]] + L[i])
    print(res[-1])
    knap_rec(res[-1], L, N)

    
if __name__ == '__main__':
    n = 3
    v = 5
    cost_list = [3, 1, 2]
    worth_list = [120, 60, 100]
    # print(bag_10(n, 3, cost_list, worth_list))
    # res = bag_10(n, v, cost_list, worth_list)[n][v]  # 要注意不要改变原输入
    # knap_rec(3, worth_list, 3)
    # print(bag_10_rec(n-1, v))
    test_list = [1, 2, 3, 4, 5, 6]
    bag_10_variant(test_list)
    
    
    
    
    
    