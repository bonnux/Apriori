#coding=utf-8

#将所有事务中出现的项组成一个集合，记为C1
def getC1(data):
    C1 = {}
    for line in data:
        for i in line:
            if i in C1:
                C1[i] += 1
            else:
                C1[i] = 1
    return C1

#根据C1求得1-频繁项集L1
def getL1(C1, minSup):
    listC1 = list(C1.keys())
    listC1.sort()
    L1 = []
    sup1 = []
    for i in listC1:
        if C1[i] >= minSup:#*getLine():
            temp = []
            temp.append(i)
            L1.append(temp)
            sup1.append(C1[i])
    return L1, sup1

#连接步，由两个L(k-1)组合成Ck的候选项集
def gen(L_old, k):
    tempC = []
    j = 0
    for i in range(len(L_old)):
        j = max(i+1, j)
        #先把两个L(k-1)直接组成一个集合
        for p in range(i+1, j):
            tempC.append(link(L_old[i], L_old[p], k))
        #再把两个可以连接的k-1项的项集组成一个k项的项集
        while j < len(L_old):
            if cheak(L_old[i], L_old[j], k):
                tempC.append(link(L_old[i], L_old[j], k))
                j += 1
            else:
                break
    return tempC

def cheak(La, Lb, k):
    for i in range(k-1):
        if(La[i] != Lb[i]):
            return False
    return True

def link(La, Lb, k):
    temp = La[:]
    temp.append(Lb[k-1])
    return temp

#剪枝步，根据连接步产生的候选项集tempC，排除其子集为非频繁的项集，得到Ck
def cut(tempC, L_old, k):
    C_new = []
    for item in tempC:
        flag = True
        i = 0
        while i < k and flag:
            temp = item[:]        #求候选项集tempC中的所有子集
            del temp[i]
            if temp not in L_old: #如果该子集不在L(k-1)中，则排除
                flag = False
            i += 1
        if flag:
            C_new.append(item)
    return C_new

#由Ck产生频繁项集Lk
def getLk(Ck, data, minSup):
    Lk = []
    sup = []
    for itemSet in Ck:
        cal = 0
        for sets in data:
            flag = True
            for item in itemSet:     #遍历Ck的全部项集
                if item not in sets: #如果Ck中有一个项集的元素不在当前的行中
                    flag = False     #则排除该项集
                if not flag:
                    break
            if flag:
                cal += 1
        if cal >= minSup:#*getLine():
            Lk.append(itemSet)
            sup.append(cal)
    return Lk, sup

#apriori算法
def apriori(data, minSup):
    L = []
    sup = []
    #求C1，L1
    C1 = getC1(data)
    L1, sup1 = getL1(C1, minSup)
    Lk = L1
    supk = sup1
    #求Ck,Lk，得出最终的频繁项集
    k = 1
    while Lk != []:
        L.append(Lk)                       #存放符合支持度的频繁项集
        sup.append(supk)                   #存放对应的支持度
        tempCk = gen(L[k - 1], k)          #由L(k-1)获得Ck候选集
        Ck = cut(tempCk, L[k - 1], k)      #由Ck候选集获得Ck
        Lk, supk = getLk(Ck, data, minSup) #由Ck获得Lk
        k += 1
    return L, sup

#读取源数据
def load():
    with open("data.txt", "rU") as f:
        d = []
        for line in f.readlines():
            d.append(line.split())
    return  d
'''
#获取行数
def getLine():
     l = len(open("data.txt", "rU").readlines())
     return l
'''
#输出结果
def output(element, sup):
    for i, element in enumerate(element):
        print(str(i+1), "- 频繁项集:")
        for j, element in enumerate(element):
            print(element, "\t\t\t", sup[i][j])
        print("\n")

if __name__ == "__main__":
    minSup = 500     #设置最小支持度
    data = load()
    L, sup = apriori(data, minSup)
    output(L, sup)