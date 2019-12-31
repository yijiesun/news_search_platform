from django.contrib import admin
from search.models import Detail, Abstract, Entry

class AbstractAdmin(admin.ModelAdmin):
    list_display = ('article_id', 'title', 'pub_time','links')#列表显示内容
    search_fields = ('article_id', 'title')#搜索框
# Register your models here.
admin.site.register(Detail)
admin.site.register(Abstract, AbstractAdmin)
admin.site.register(Entry)