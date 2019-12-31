#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import sys
import re
import pandas as pd
import os
import random
import time

reload(sys)
sys.setdefaultencoding('utf-8')
ty = sys.getfilesystemencoding()
dir = 'result/'
csv = pd.read_csv(dir+'info.csv')
ID = len(csv)
linkList = []
#http://world.people.com.cn/n1/2018/0911/c1002-30284709.html

def initLinkList():
	f = open(dir + 'list.txt')
	global linkList
	contents = f.readlines()
	for con in contents:
		con = con.replace('\r','').replace('\n','')
		linkList.append(con)
	print linkList

def getTitle(content):
	pat_title = re.compile(r'<title>(.*?) </title>')
	items = re.findall(pat_title, content)
	title = ""
	if (len(items) != 1):
		print("title error", items)
		return None
	else:
		title = items[0]
	return title

def getArticle(content):
	pat1 = re.compile(r'<div class="box_con" id="rwb_zw">.*?(<[p|P].*?)<div', re.DOTALL)
	items = re.findall(pat1, content)
	raw = ""
	if (len(items) != 1):
		print("article range error", items)
		return None
	else:
		raw = items[0]
	pat2 = re.compile(r'<[Pp].*?>(.*?)</[Pp]>', re.DOTALL)
	#pat2 = re.compile(r'<P>(.*?)</P>', re.DOTALL)
	items = re.findall(pat2, raw)
	#print items
	ret = ""
	for item in items:
		matches = re.search(r' |	|(<.*>)|(&nbsp;)', item)
		while matches is not None:
			item = item.replace(matches.group(0), '')
			matches = re.search(r' |	|(<.*>)|(&nbsp;)', item)
		lines = re.findall('.*', item)
		for l in lines:
			if len(l)>0:
				ret = ret+l+'\r\n'
	#print ret
	return ret

def getTime(content):
	pat = re.compile(r'<div class="fl">(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)')
	tm = re.findall(pat, content)
	if len(tm) != 1:
		print "time error"
		return None
	ret = map(lambda x: int(x), tm[0])
	return ret

def getLink(content):
	pat1 = re.compile(r'<div class="clearfix box_news">(.*?)</div>', re.DOTALL)
	raw = re.findall(pat1, content)
	if len(raw) != 1:
		print "link range error"
		return None
	#print 'raw:', raw[0]

	pat2 = re.compile(r'<li><a href="(.*?)" target="_blank">(.*?)</a></li>')
	links = re.findall(pat2, raw[0])
	# print links
	# print 'links:'
	# for link in links:
	# 	print link[0], link[1]
	return links

def getPage(ID, url):
	print 'now getting', ID, ":", url
	try:
		data = requests.get(url)
	except:
		print "error network"
		return
	data.encoding = 'GBK'
	content = data.text
	#print content

	title = getTitle(content)
	article = getArticle(content)
	time = getTime(content)
	links = getLink(content)
	if (title is None) or (article is None) or (time is None) or (links is None):
		return

	# dir = str(ID)+'/'
	# if not os.path.exists(dir):
	# 	os.makedirs(dir)

	f = open(dir + "%d.html"%ID, "w")
	f.write(content)
	f.close()

	f = open(dir + "%d.txt"%ID, "w")
	f.write(article)
	f.close()

	linkPD =pd.DataFrame(links)
	linkPD.columns = ['url', 'title']
	#print linkPD
	linkPD.to_csv(dir + "%d.csv"%ID, index = False)

	newRow = [ID, title] + time +[url]
	#print newRow
	global csv
	csv.loc[ID] = newRow
	csv.to_csv(dir + 'info.csv', index = False)

	global linkList
	for url in linkPD.url:
		if len(csv[csv.url.str.contains(url)]) == 0 and url not in linkList:
			linkList.append(url)

	f = open(dir + 'list.txt', "w")
	for url in linkList:
		f.write(url+'\r\n')
	f.close()

initLinkList()
while len(linkList) != 0:
	Url = linkList[0]
	del linkList[0]
	#Url = 'http://world.people.com.cn/n1/2018/0613/c1002-30053562.html'
	getPage(ID, Url)
	ID = len(csv)
	time.sleep(random.random()+0.5)
	#break

# print url
# getPage(url)
