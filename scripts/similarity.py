import pandas as pd
import csv
import os
import math

# c = csv.reader(open("../result/mix.csv", encoding='UTF8'))
# db = []
# for x in c:
#     db.append(x)
# db[0]= ['idx']+db[0]+['idf']
# n = 10000
# for i in range(1,len(db)):
#     l = len(db[i][1].split('|'))
#     db[i] = ['%d' %(i-1)]+db[i]+[str(math.log(n/l))]
# f = open('../result/mix1.csv', 'w', encoding='utf-8', newline='')
# w = csv.writer(f)
# w.writerows(db)

c = csv.reader(open("../result/mix.csv", encoding='UTF8'))
db = []
for x in c:
    db.append(x)
db = db[1:]
dic = {}
for x in db:
    dic[x[1]] = int(x[0])
print(dic)

idf = [float(x[4]) for x in db]
sz = [os.path.getsize('../result/text/%d.txt' % x) for x in range(10000)]
#print(sz)
seg = [[] for x in range(10000)]
for i in range(10000):
    if i % 100 == 0:
        print("loading %d" %i)
    c = csv.reader(open("../result/seg_id/%d.csv" % i, encoding='UTF8'))
    is_first = 1
    for x in c:
        if is_first:
            is_first = 0
            continue
        seg[i].append((int(x[0]), int(x[2])*1.0/sz[i])) # id, frequency
    seg[i].sort()
print(seg[0])
print(seg[0][0], seg[0][1])
print("read finish")

for i in range(2531, 10000):
    print("now solving %d" % i)
    simi = []
    if len(seg[i]) == 0:
        continue
    for j in range(10000):
        # print("j %d" % j)
        if i == j:
            continue
        l1 = 0
        r1 = len(seg[i])
        l2 = 0
        r2 = len(seg[j])
        inter = 0.0
        union = 0.0
        while l1 < r1 or l2 < r2:
            if l1 < r1 and l2 < r2 and seg[i][l1][0] == seg[j][l2][0]:
                # print('same %d' % seg[i][l1][0])
                # print(idf[seg[i][l1][0]], seg[i][l1][1], seg[j][l2][1], min(seg[i][l1][1], seg[j][l2][1]))
                inter += idf[seg[i][l1][0]]*min(seg[i][l1][1], seg[j][l2][1])
                union += idf[seg[i][l1][0]]*max(seg[i][l1][1], seg[j][l2][1])
                l1 += 1
                l2 += 1
            elif l2 >= r2 or (l1 < r1 and seg[i][l1][0] < seg[j][l2][0]):
                # print('diff0: %d' %seg[i][l1][0])
                union += idf[seg[i][l1][0]]*seg[i][l1][1]
                l1 += 1
            else:
                # print('diff1: %d' %seg[j][l2][0])
                union += idf[seg[j][l2][0]]*seg[j][l2][1]
                l2 += 1
        simi.append((inter/union, j))
    simi.sort(reverse=True)
    #print(simi)
    f = open('../result/similarity/%d.csv' % i, 'w', encoding='utf-8', newline='')
    f.write('jaccard,idx\n')
    w = csv.writer(f)
    w.writerows(simi)

# for i in range(10000):
#     print("now %d" % i)
#     c = csv.reader(open("../result/seg/%d.csv" % i, encoding='UTF8'))
#     seg = []
#     for x in c:
#         seg.append(x)
#     ans = [['idx']+seg[0]]
#     for j in range(1, len(seg)):
#         if int(seg[j][1]) <= 1:
#             continue
#         ans.append([str(dic[seg[j][0]])]+seg[j])
#     f = open('../result/seg_id/%d.csv' % i, 'w', encoding='utf-8', newline='')
#     w = csv.writer(f)
#     w.writerows(ans)

