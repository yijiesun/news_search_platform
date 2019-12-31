import sqlite3
import csv

# con = sqlite3.connect('D:/codes/xiaoxueqi/week3/web/db.sqlite3')
# c = con.cursor()
# cv = csv.reader(open("../result/mix.csv", encoding='UTF8'))
# log = []
# for item in cv:
#     log.append(item)

# for i in range(1):
#     print("now %d" %i)
#     st = "INSERT INTO SEARCH_ENTRY (WORD,LINKS,TIMES) \
#           VALUES ('%s', '%s', '%s')" % (log[i][0],log[i][1],log[i][2])
#     #print(st)
#     c.execute(st)

# for i in range(1,10000):
#     print("now %d" %i)
#     st = 'INSERT INTO SEARCH_ABSTRACT (ARTICLE_ID,TITLE,PUB_TIME,ABSTRACT) \
#           VALUES (%d, "%s", "%s-%s-%s %s:%s:00", "")' % (i,log[i][1],log[i][2],log[i][3],log[i][4],log[i][5],log[i][6])
#     print(st)
#     c.execute(st)


# for i in range(1):
# 	print("now %d" %i)
# 	f = open('../result/text/%d.txt' %i, encoding='UTF8', newline='')
# 	text = ""
# 	for t in f.readlines():
# 		text = text+t.strip('\n')+' '
# 	if len(text)>170:
# 		text = text[:170]
# 	text = text.replace("'",' ')

# 	st = "UPDATE SEARCH_ABSTRACT set ABSTRACT = '%s' where ARTICLE_ID=%d" % (text, i)
# 	#print(st)
# 	c.execute(st)


# cv = csv.reader(open("../result/info.csv", encoding='UTF8'))
# log = []
# for item in cv:
#     log.append(item)
# log = log[1:]
# for i in range(10000):
# 	st = "UPDATE SEARCH_ABSTRACT set PUB_TIME = '%04d-%02d-%02d %02d:%02d:00' where ARTICLE_ID=%d" \
# 	% (int(log[i][2]), int(log[i][3]), int(log[i][4]), int(log[i][5]), int(log[i][6]), i)
# 	print(st)
# 	c.execute(st)

# insert links
con = sqlite3.connect('D:/codes/xiaoxueqi/week3/web/db.sqlite3')
c = con.cursor()
for i in range(10000):
	print("now %d" %i)
	try:
		cv = csv.reader(open("../result/similarity/%d.csv" %i, encoding='UTF8'))
	except:
		print("no %d" %i)
		continue
	log = []
	for item in cv:
	    log.append(str(item[1]))
	if len(log) > 1:
		s = "|".join(log[1:min(len(log), 4)])
		st = "UPDATE SEARCH_ABSTRACT set LINKS = '%s' where ARTICLE_ID=%d" % (s, i)
		con.execute(st)
con.commit()
