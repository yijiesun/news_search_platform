import jieba
import csv
import sqlite3


def run1():
    c = csv.reader(open("../result/mix.csv", encoding='UTF8'))
    mix = []
    for con in c:
        mix.append(con)
    mix = mix[1:]
    print(mix[:10])

    info = []
    c = csv.reader(open("../result/info.csv", encoding='UTF8'))
    for con in c:
        info.append(con)
    info = info[1:]
    print(info[:10])

    dict = {}
    for x in mix:
        dict[x[1]] = int(x[0])

    for i in range(0, 10000):
        st = info[i][1]
        # print(st)
        cut = jieba.cut_for_search(st)
        for c in cut:
            # print(c)
            if c in ['-', '：', '“', '”', "'"]:
                continue
            if c in dict:
                id = dict[c]
                # print(id, mix[id])
                mix[id][2] += '|' + str(i)
                mix[id][3] += '|5'
            else:
                n = len(mix)
                mix.append([str(n), c, str(i), '5', '0.0'])
                dict[c] = n
                print('new word: %s %d %d' % (c, n, len(mix)))

    f = open('../result/mix_title.csv', 'w', encoding='utf-8', newline='')
    w = csv.writer(f)
    f.write('idx,word,idx,time,idf\n')
    w.writerows(mix)
    f.close()


def run2():
    c = csv.reader(open("../result/mix_title.csv", encoding='UTF8'))
    mix = []
    for con in c:
        mix.append(con)
    mix = mix[1:]
    print(mix[:10])
    for t in range(0, len(mix)):
        x = mix[t]
        st1 = x[2].split('|')
        st2 = x[3].split('|')
        dict = {}
        for i in range(0, len(st1)):
            if st1[i] in dict:
                dict[st1[i]] += int(st2[i])
            else:
                dict[st1[i]] = int(st2[i])
        lst = []
        for i in dict:
            lst.append([dict[i], i])
        lst.sort(reverse=True)
        s1 = ""
        s2 = ""
        for x in lst:
            if s1 != '':
                s1 += '|'
            if s2 != '':
                s2 += '|'
            s1 += x[1]
            s2 += str(x[0])
        mix[t][2] = s1
        mix[t][3] = s2

    f = open('../result/mix_title_sort.csv', 'w', encoding='utf-8', newline='')
    w = csv.writer(f)
    f.write('idx,word,idx,time,idf\n')
    w.writerows(mix)
    f.close()


def run3():
    c = csv.reader(open("../result/mix_title_sort.csv", encoding='UTF8'))
    mix = []
    for con in c:
        mix.append(con)
    mix = mix[1:]
    con = sqlite3.connect('D:/codes/xiaoxueqi/week3/web/db.sqlite3')
    c = con.cursor()
    for i in range(31371, len(mix)):
        #st = "UPDATE SEARCH_ENTRY set LINKS = '%s', TIMES = '%s' where ID=%d" % (mix[i][2], mix[i][3], i+1)
        st ="INSERT INTO SEARCH_ENTRY (WORD,LINKS,TIMES) VALUES ('%s', '%s', '%s')" % (mix[i][1], mix[i][2], mix[i][3])
        con.execute(st)
    con.commit()

def run4():
    cv = csv.reader(open("../result/info1.csv", encoding='UTF8'))
    info = []
    for con in cv:
        info.append(con)
    info = info[1:]
    con = sqlite3.connect('D:/codes/xiaoxueqi/week3/web/db.sqlite3')
    c = con.cursor()
    print(len(info))
    print(info[8637])
    for i in range(0, len(info)):
        st = "UPDATE SEARCH_ABSTRACT set TITLE = '%s' where ARTICLE_ID=%d" % (info[i][1], i)
        print(st)
        con.execute(st)
    con.commit()


for i in range(0, 10000):
    f = open('../result/text/%d.txt' % i, encoding='UTF-8')
    st = f.read()
    if st.find('&') != -1:
        print(i, st.find('&'))
