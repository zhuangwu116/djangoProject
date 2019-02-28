from datetime import datetime

from django.db import models

from django.contrib.auth import get_user_model

from blogs.models import BlogsArticle

User = get_user_model()
# Create your models here.
class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(User, verbose_name="用户")
    articles = models.ForeignKey(BlogsArticle, verbose_name="文章", help_text="文章id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
        unique_together = ("user", "articles")
    def __str__(self):
        return self.user.username