from django.db import models


class Detail(models.Model):
    article_id = models.IntegerField()
    text = models.CharField(max_length=25000, default="")
    links = models.CharField(max_length=50, default="") #8*(4+1)
    def __str__(self):
        return self.article_id

class Abstract(models.Model):
    article_id = models.IntegerField()
    title = models.CharField(max_length=100)
    pub_time = models.DateTimeField()
    abstract = models.CharField(max_length=150, default="")
    links = models.CharField(max_length=100, default="")
    #detail = models.ForeignKey(Detail, on_delete=models.CASCADE)


class Entry(models.Model):
    word = models.CharField(max_length=10)
    links = models.CharField(max_length=30000)
    times = models.CharField(max_length=30000)
