from datetime import datetime


from django.db import models
from django.contrib.auth import get_user_model



from DjangoUeditor.models import UEditorField



User = get_user_model()
# Create your models here.
# tag（标签）
class BlogsTag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

# 分类
class BlogsCategory(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=999,verbose_name='分类的排序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

# 自定义一个文章Model的管理器
# 1、新加一个数据处理的方法
# 2、改变原有的queryset
class BlogsArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m文章存档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list

# 文章模型
class BlogsArticle(models.Model):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = UEditorField(verbose_name=u"文章内容", imagePath="article/images/", width=1000, height=300,
                              filePath="article/files/", default='')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户')
    category = models.ForeignKey(BlogsCategory,  verbose_name='分类')
    tag = models.ManyToManyField(BlogsTag, verbose_name='标签')

    objects = BlogsArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name


    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title
# 评论模型
class BlogsComment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, verbose_name='用户')
    article = models.ForeignKey(BlogsArticle, verbose_name='文章')
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)
    def __str__(self):
        return self.content