from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    text = models.TextField(blank=True, default='')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, default='')
    text = models.TextField(blank=True, default='')
