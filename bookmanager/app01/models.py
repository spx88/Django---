from django.db import models

# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=32)

class Book(models.Model):
    name = models.CharField(max_length=32)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE) #默认是级联删除

    """级联删除 on_delete=models.CASCADE  主键删除 主键关联的外键都删除
        保护 on_delete=models.PROTECT     删除所有外键后才能删除相关主键
        on_delete=models.SET()  删除后设置为某一个值\
    """

class Author(models.Model):
    name = models.CharField(max_length=32)
    books = models.ManyToManyField('Book')  #多对多关系的快捷方法，会创建第三张表

