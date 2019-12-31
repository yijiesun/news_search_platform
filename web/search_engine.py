import sqlite3
import math

def get_target_id(input_text):
    con = con = sqlite3.connect('/home/syj/django/news_search/web/db.sqlite3')
    c = con.cursor()
    result = {}
    threshold_time = threshold_text = 0
    text = input_text.split()

    for x in text:
        print(x)
        if x[0] == '&':
            threshold_time = 20000
            st = 'SELECT ARTICLE_ID FROM SEARCH_ABSTRACT WHERE DATETIME(PUB_TIME) BETWEEN DATETIME("%s") AND DATETIME("%s", "+1 day", "-1 second")' %(x[1:11], x[12:22])
            c.execute(st)
            for row in c:
                if row[0] in result:
                    result[row[0]] += 20000
                else:
                    result[row[0]] = 20000.0

        else:
            threshold_text = 1000
            st = 'SELECT LINKS,TIMES FROM SEARCH_ENTRY WHERE WORD="%s"' % x
            c.execute(st)
            for row in c:
                #print(row)
                ID = row[0].split('|')
                tm = row[1].split('|')
                for i in range(0, len(ID)):
                    if int(ID[i]) in result:
                        result[int(ID[i])] += 1000 + math.log(int(tm[i]))
                    else:
                        result[int(ID[i])] = 1000.0 + math.log(int(tm[i]))
    print(result)
    threshold = threshold_text + threshold_time
    mid = []
    for r in result:
        if result[r] >= threshold:
            mid.append((result[r], r))
    mid.sort(reverse=True)
    ans = [x[1] for x in mid]
    return ans



if __name__ == '__main__':
    print(get_target_id('俄罗斯 中国'))

