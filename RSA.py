'''
RSA加密解密算法：场景模拟
1、receiver生成两个秘钥：公钥(n, e)和私钥(n, d)
2、receiver将公钥发送给sender，并保留自己的私钥
3、sender用公钥将明文m进行加密，得到密文c
4、sender将密文c发送给receiver（密文c可能会被监听、篡改）
5、receiver用自己的私钥对密文c进行解密，得到解密后的明文m
'''
import math, time
from decimal import Decimal
# 欧拉函数通式：求小于等于n的正整数中与n互质的个数：φ(n) = n(1-1/p1)(1-1/p2)…(1-1/pr)
def Euler_func(n):
    prims_factor = find_prims_factor(n=n)
    s = 1.0
    for factor in prims_factor:
        s *= (1 - 1 / factor)
    return int(n * s)
# 欧拉定理：若a,b为正整数，且a,b互质 => a**m mod b = 1，其中：m = Euler_func(b)
def Euler_theorem(a, b):
    return a**Euler_func(b) % b
# 欧几里得算法：求a和b的最大公约数
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
# 拓展欧几里得非递归算法：求二元一次方程的通解：ax + by = gcd(a, b)
def ex_gcd(a, b):
    if b == 0:
        return 1, 0
    x1, y = 1, 1
    x, y1 = 0, 0
    c, d = a, b
    q = int(c / d)
    r = c % d
    while r != 0:
        c = Decimal(d)
        d = r
        x1, x = x, x1 - x * q
        y1, y = y, y1 - y * q
        q = int(c / d)
        r = int(c) % d
    return x, y
# 大整数求模：快速幂算法：a^b % n
def poww_mod(a, b, mod):
    res = 1
    while b != 0:
        if b & 1 == 1:
            res = res * a % mod
        a = a * a % mod
        b >>= 1  # 遍历b的二进制位
    return res
# 寻找范围n以内的所有质数——筛选法
def find_prims(n):
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
# 寻找n的所有质因数：每个合数都可以写成几个质数相乘的形式
def find_prims_factor(n):
    prims = find_prims(n=n)  # 先找出n以内所有的质数
    prims_factor = []
    for p in prims:
        r = 1
        while p**r <= n:
            if n % p**r == 0:
                prims_factor.append(p)
                break
            r += 1
    return prims_factor
# oop模拟receiver
class Receiver:
    def __init__(self):
        self.create_pub_pri_key()
    # 生成秘钥：私钥+公钥的策略
    def create_pub_pri_key(self):
        # 随机选取两个不相等的质数
        p, q = 8887, 13163
        # 计算二者的乘积
        n = p * q
        # 当p和q都是质数的情况，则欧拉函数φ(n) = φ(p*q) = φ(p) * φ(q) = (p - 1) * (q - 1)
        fi = (p - 1) * (q - 1)
        # 随机选择一个整数e：1 < e < fi and e和fi互质
        e = 65537
        # 计算e对于fi的模反元素d
        d = max(ex_gcd(a=Decimal(fi), b=e))
        # 得到公钥和私钥
        self.pub_key, self.pri_key = (n, e), (n, d)
    def get_pub_key(self):
        return self.pub_key
    def decode_c(self, c):
        n, d = self.pri_key
        m = poww_mod(c, d, n)  # m = c**d % n，对密文c进行解密，得到明文m
        return m
# oop模拟sender
class Sender:
    def __init__(self, pub_key):
        self.pub_key = pub_key
    # 用receiver的公钥对明文m进行加密
    def encode_m(self, m):
        n, e = self.pub_key
        if m >= n:
            return None
        c = poww_mod(m, e, n)  # c = m**e % n，对明文m进行加密，得到密文c
        return c
# oop模拟窃听者
class Hacker:
    def __init__(self):
        pass
    def crack(self, pub_key, c):
        n, e = pub_key
        p, q = find_prims_factor(n=n)  # 质因数分解合数n(非常困难)
        fi = (p - 1) * (q - 1)
        d = max(ex_gcd(a=Decimal(fi), b=e))
        m = poww_mod(c, d, n)
        return m
if __name__ == '__main__':
    start = time.clock()
    receiver = Receiver()  # 接收方
    pub_key = receiver.get_pub_key()  # 获取接收方生成的公钥
    sender = Sender(pub_key=pub_key)  # 发送方
    c = sender.encode_m(m=123456)  # 发送方将明文m进行加密，得到密文c
    m = receiver.decode_c(c=c)  # 接收者将密文c进行解密，得到明文m
    print('公共环境暴露的公钥为：{}，密文为：{}'.format(pub_key, c))
    print('RSA解密的明文为：{}，加密解密花费的时间为：{}秒'.format(m, round(time.clock() - start, 2)))
    # 破解密文c的过程
    # start = time.clock()
    # hacker = Hacker()  # 窃听者
    # m2 = hacker.crack(pub_key=pub_key, c=c)
    # print('破解密文后的明文为：{}，花费的时间为：{}秒'.format(m2, round(time.clock() - start, 2)))
