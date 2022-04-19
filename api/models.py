from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import Group
import mptt


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    text = models.TextField(blank=True, default='')


# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, default='')
#     text = models.TextField(blank=True, default='')
#     previous_comment = models.PositiveIntegerField(blank=True, null=True, default=None)
#     #previous_comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, blank=True, null=True)

class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(blank=True, default='')
    parent = TreeForeignKey("Comment", blank=True, null=True, on_delete=models.SET_NULL, default=None,
                            related_name='children')
    lft = models.PositiveIntegerField(default=None, null=True)
    rght = models.PositiveIntegerField(default=None, null=True)
    tree_id = models.PositiveIntegerField(default=None, null=True)
    level = models.PositiveIntegerField(default=None, null=True)
    mptt.register(Group, order_insertion_by=['name'])
