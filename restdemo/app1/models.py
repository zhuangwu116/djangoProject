from django.db import models
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class UserGroup(models.Model):
    title = models.CharField(max_length=32)

class UserInfo(models.Model):
    user_type_choices=((1,'普通用户'),
                       (2,'VIP'),
                       (3,'SVIP'),)
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    group = models.ForeignKey('UserInfo', on_delete=models.PROTECT)
    roles = models.ManyToManyField('Role')

class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

class Role(models.Model):
    title = models.CharField(max_length=32)


class Course(models.Model):
    title = models.CharField(max_length=32)


class DegreeCourse(models.Model):
    title = models.CharField(max_length=32)

class PricePolicy(models.Model):
    price = models.IntegerField()
    period = models.IntegerField()

    # table_name = models.CharField(verbose_name='关联的表名称')
    # object_id = models.CharField(verbose_name='关联的表中的数据行的ID')
    content_type = models.ForeignKey(ContentType, verbose_name='关联的表名称')
    object_id = models.IntegerField(verbose_name='关联的表中的数据行的ID')
    content_object = Gen


