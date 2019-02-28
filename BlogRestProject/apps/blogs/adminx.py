import xadmin

from .models import BlogsTag, BlogsCategory, BlogsArticle, BlogsComment

class BlogsTagAdmin(object):
    list_display = ["name", "add_time"]

class BlogsCategoryAdmin(object):
    list_display = ["name", "index", "add_time"]

class BlogsArticleAdmin(object):
    list_display = ["title", "desc", "content", "click_count", "is_recommend",
                    "date_publish"]
    search_fields = ['title', ]
    list_editable = ["is_recommend", ]
    list_filter = ["title", "desc", "click_count", "is_recommend", "date_publish", "category__name",
                   "user", "tag__name"]
    style_fields = {"content": "ueditor"}


class BlogsCommentAdmin(object):
    list_display = ["content", "date_publish"]
    list_filter = ["article__title", "user__username", "date_publish"]


xadmin.site.register(BlogsTag, BlogsTagAdmin)

xadmin.site.register(BlogsCategory, BlogsCategoryAdmin)

xadmin.site.register(BlogsArticle, BlogsArticleAdmin)

xadmin.site.register(BlogsComment, BlogsCommentAdmin)

