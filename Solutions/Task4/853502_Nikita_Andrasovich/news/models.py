from django.db import models
from django.contrib.auth.models import User


class NewsThread(models.Model):
    thread_name = models.CharField(max_length=20)

    def __str__(self):
        return self.thread_name


class News(models.Model):
    title = models.CharField(max_length=25)
    pub_date = models.DateTimeField()
    content = models.TextField()
    thread = models.ForeignKey(
        NewsThread, on_delete=models.CASCADE, related_name='news')

    def __str__(self):
        return self.title + " - " + str(self.pub_date)


class NewsSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(NewsThread, on_delete=models.CASCADE)
