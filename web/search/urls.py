from  django.urls import path
from . import views


app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:idx>', views.index, name='index_number'),
    path('article/<int:idx>', views.article, name='article'),
    path('search/', views.search, name='search'),
]
