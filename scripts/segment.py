import jieba
from collections import Counter
import pandas as pd
import csv

def seg(id):
    print("segmenting %d" % id)
    f = open('input/%d.txt' % id, 'r', encoding='UTF-8')
    text = f.read()
    cut = jieba.cut_for_search(text)
    realWords = [x for x in cut if len(x) >= 2]
    c = Counter(realWords)
    word = []
    tm = []
    for dt in c:
        word.append(dt)
        tm.append(c[dt])
    df = pd.DataFrame({
        'word': word,
        'times': tm
    })
    df.to_csv('output/seg%d.csv' % id, index=False)


def getID(url):
    #print(url)
    global db
    #print(db['url']==url)
    se = db[db['url'] == url].id
    if len(se) == 0:
        return -1
    if len(se) > 1:
        print("too many urls ", url)
    for j in se:
        #print(j)
        return j


def urlID(id):
    global db
    csv = pd.read_csv('../result/csv/%d.csv' % id)
    csv['urlID'] = csv.apply(lambda x:getID(x.url), axis=1)
    csv.to_csv('../result/idcsv/%d.csv'%id)


def sortSeg(id):
    print("sorting %d" % id)
    csv = pd.read_csv('../result/segg/seg%d.csv' % id)
    csv.sort_values('times', inplace=True, ascending=False)
    csv.to_csv("../result/seg/%d.csv" % id, index=False)


def delIndex(id):
    csv = pd.read_csv('../result/idcsv/%d.csv' % id, index_col=0)
    csv.to_csv('../result/idcsv/%d.csv' % id, index=False)


def getLinkNumber(id):
    print("getting %d", id)
    cv = pd.read_csv('../result/idcsv/%d.csv' % id)
    return len(cv[cv['urlID'] != -1])


def addLink():
    csv = pd.read_csv('../result/info.csv')
    print(len(csv))
    csv['link'] = csv.apply(lambda x: getLinkNumber(x['idx']), axis = 1)
    csv.to_csv('../result/info1.csv', index=False)


def extend(x, item, id):
    if x.word != item.word:
        return x
    x.time = str(x.time) + '|' + str(item.times)
    x.link = str(x.link) + '|' + str(id)
    return x

# def mixTable():
#     table = pd.DataFrame({
#         'word': [""],
#         'link': [""],
#         'time': [""]
#     })
#     print(table)
#     used = 0
#     for i in range(10000):
#         print("solve %d" % i)
#         seg = pd.read_csv('../result/seg/%d.csv' % i)
#         for j in range(0, len(seg)):
#             item = seg.loc[j]
#             if item['times'] <= 1:
#                 continue
#             if len(table[table['word'] == item['word']]) == 0:
#                 newRow = [item['word'], str(i), str(item['times'])]
#                 n = len(table)
#                 if used == 0:
#                     n = 0
#                     used = 1
#                 table.loc[n] = newRow
#             else:
#                 table = table.apply(lambda x: extend(x, item, i), axis=1)
#
#                 # table.loc[table['word'] == item.word].apply() = \
#                 #     table.loc[table['word'] == item.word].time + '|' + str(item.times)
#                 # table.loc[table['word'] == item.word].link = \
#                 #     table.loc[table['word'] == item.word].link + '|' + str(i)
#     table.to_csv('../result/mix.csv')


def mixTable():
    word = {}
    for i in range(10000):
        print("now %d" %i)
        c = csv.reader(open("../result/seg/%d.csv" % i, encoding='UTF8'))
        is_head = True
        for content in c:
            if is_head:
                is_head = False
                continue
            if int(content[1]) <= 1:
                continue
            if content[0] in word:
                word[content[0]].append((i, int(content[1])))
            else:
                word[content[0]] = [(i, int(content[1]))]
    f = open('../result/mix.csv', 'w', encoding='utf-8', newline='')
    w = csv.writer(f)
    ans = []
    for item in word:
        word[item].sort(key = lambda x:x[1], reverse=True)
        lst0 = [str(x[0]) for x in word[item]]
        idx = '|'.join(lst0)
        lst1 = [str(x[1]) for x in word[item]]
        tm = '|'.join(lst1)
        ans.append([item, idx, tm])
    #print(ans)
    w.writerows(ans)


mixTable()
