import xadmin
from xadmin import views
from .models import Links, Ad

class LinksAdmin(object):
    list_display = ['title', 'description', "callback_url", "date_publish", "index"]

class AdAdmin(object):
    list_display = ['title', 'description', "image_url", "callback_url", "date_publish", "index"]

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "博客后台"
    site_footer = "blogproject"


xadmin.site.register(Links, LinksAdmin)
xadmin.site.register(Ad, AdAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)