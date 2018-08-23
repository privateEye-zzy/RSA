'''
RSA加密解密算法：数论基础
包含：素数筛选法、欧拉函数、欧几里得算法，欧几里得扩展算法、大整数快速幂/快速幂取模算法
'''
import math, time
import matplotlib.pyplot as plt
# 在所有质数因子里，判断x是否是质数
def is_prim_in_prims(x, prims):
    sqx = math.sqrt(x)
    for p in prims:
        if p <= sqx and x % p == 0:
            return False
        if p > sqx:
            return True
# 短除算法——严进宽出
def find_prim_method1(n):
    prims = [2]
    for x in range(3, n, 2):
        if is_prim_in_prims(x, prims) is True:
            prims.append(x)
    return prims
# 筛选法——宽进严出
def find_prim_method2(n):
    prims_bool = [False, False] + [True] * (n - 1)
    for i in range(3, len(prims_bool)):
        if i & 1 == 0:  # 将所有下标为偶数的置为False
            prims_bool[i] = False
    for i in range(3, int(math.sqrt(n)) + 1):
        if prims_bool[i] is True:
            for j in range(i + i, n + 1, i):  # 将质数i的倍数全部置为False
                prims_bool[j] = False
    prims = []
    [prims.append(i) for i, v in enumerate(prims_bool) if v is True]
    return prims
# 素数螺旋
def prim_draw(prims):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    xs, ys = [], []
    for p in prims:
        xs.append(p * math.cos(p))
        ys.append(p * math.sin(p))
    ax1.scatter(xs, ys, color='red')
    plt.show()
# 欧几里得算法：求a和b的最大公约数
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
# 欧几里得拓展算法：求ax+by=gcd(a，b)的一个解(x，y)
def ex_gcd(a, b):
    if b == 0:
        return 1, 0
    x1, y = 1, 1
    x, y1 = 0, 0
    c, d = a, b
    q = int(c / d)
    r = c % d
    while r != 0:
        c = d
        d = r
        x1, x = x, x1 - x * q
        y1, y = y, y1 - y * q
        q = int(c / d)
        r = c % d
    return x, y
# 大整数快速幂算法：a^b
def poww(a, b):
    res = 1
    while b > 0:
        if b & 1 == 1:
            res *= a
        a *= a
        b >>= 1
    return res
# 大整数快速幂求模算法：a^b % mod
def poww_mod(a, b, mod):
    res = 1
    while b != 0:
        if b & 1 == 1:
            res = res * a % mod
        a = a * a % mod
        b >>= 1
    return res
if __name__ == '__main__':
    # ************************测试素数算法************************#
    n = 2 ** 22  # 295947个质数
    start = time.clock()
    prims = find_prim_method1(n=n)
    print('短除算法：在n={}范围之内，花费了：{}秒，找到：{}个质数'.
          format(n, round(time.clock() - start, 2), len(prims)))
    start = time.clock()
    prims = find_prim_method2(n=n)
    print('筛选算法：在n={}范围之内，花费了：{}秒，找到：{}个质数'.
          format(n, round(time.clock() - start, 2), len(prims)))
    #************************测试欧几里得拓展算法************************#
    # print('欧几里得拓展算法：方程47x+30y=1的整数解为：{}'.format(ex_gcd(47, 30)))
    # ************************测试快速幂算法************************#
    # a, b = 12345678, 56789
    # start = time.clock()
    # res = poww(a=a, b=b)
    # print('计算{}^{}：快速幂算法耗时：{}'.format(a, b, round(time.clock() - start, 2)))
    # start = time.clock()
    # res = 1
    # for i in range(b):
    #     res *= a
    # print('计算{}^{}：直接幂连乘耗时：{}'.format(a, b, round(time.clock() - start, 2)))
    # ************************测试快速幂取模算法************************#
    # a, b, mod = 123456789, 987654, 65537
    # start = time.clock()
    # res = poww_mod(a=a, b=b, mod=mod)
    # print('计算{}^{} % {}：快速幂取模算法耗时：{}'.format(a, b, mod, round(time.clock() - start, 2)))
    # start = time.clock()
    # res = a**b % mod
    # print('计算{}^{} % {}：直接幂连乘取模耗时：{}'.format(a, b, mod, round(time.clock() - start, 2)))
