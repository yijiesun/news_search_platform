from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Abstract
from random import randint
from django.urls import reverse
from search_engine import get_target_id
import time


class WaitingList:
    lst = [i for i in range(10000)]
    article_cnt = 5
    search_text = ""
    run_time = 0.0
    @staticmethod
    def get_page(pg):
        L = len(WaitingList.lst)
        if L == 0:
            return None
        pg = max(pg, 0)
        pg = min(pg, (L-1)//WaitingList.article_cnt)
        return WaitingList.lst[pg*WaitingList.article_cnt: min((pg+1)*WaitingList.article_cnt, L)]


def index(request, idx=""):
    page = 0
    if idx != "":
        page = int(idx)
    if idx == "":
        WaitingList.lst = [i for i in range(10000)]
        WaitingList.search_text = ""
    article_list = []
    id_list = WaitingList.get_page(page)
    if id_list is None:
        article_list = None
    else:
        for i in id_list:
            article_list.append(Abstract.objects.get(article_id=i))
    context = {}
    if id_list is not None:
        context['article_list'] = article_list[:-1]
        context['article_list_end'] = [article_list[-1]]
        L = (len(WaitingList.lst)-1)//WaitingList.article_cnt
        context['cur_page'] = str(page)
        if page != 0:
            context['last_page'] = str(page-1)
        if page < L:
            context['next_page'] = str(page+1)
        if L<=9:
            context['page_range'] = [str(x) for x in range(0, L+1)]
        elif page<=5:
            context['page_range'] = [str(x) for x in range(0, 10)]
        elif page+4>L:
            context['page_range'] = [str(x) for x in range(L-9, L+1)]
        else:
            context['page_range'] = [str(x) for x in range(page-5, page+5)]
    search_text_reg = ""
    lst = WaitingList.search_text.split()
    for x in lst:
        if x[0] == '&':
            continue
        if search_text_reg != "":
            search_text_reg += '|'
        search_text_reg += x
    if search_text_reg != "":
        search_text_reg = "(%s)" % search_text_reg
    context['search_text_reg'] = search_text_reg
    context['search_time'] = '%.3f' % WaitingList.run_time
    context['search_items'] = len(WaitingList.lst)
    return render(request, 'search/index.html', context)


def article(request, idx):
    abstract = get_object_or_404(Abstract, article_id=idx)
    f = open('text/%s.txt' % idx, 'r', encoding='UTF8', newline='')
    text = f.readlines()
    recommend_id = abstract.links.split('|')
    context = {
        'title': abstract.title,
        'pub_time': abstract.pub_time,
        'text': text,
        'recommend': [Abstract.objects.get(article_id=i) for i in recommend_id]
               }
    return render(request, 'search/article.html', context)


def search(request):
    text = request.POST['search']
    time_start = time.time()
    WaitingList.lst = get_target_id(text)
    time_end = time.time()
    WaitingList.run_time = time_end - time_start
    WaitingList.search_text = text
    return HttpResponseRedirect(reverse('search:index_number', args=(0,)))
