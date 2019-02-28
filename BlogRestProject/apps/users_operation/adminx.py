import xadmin

from .models import UserFav


class UserFavAdmin(object):
    list_display = ['user', 'articles', "add_time"]


xadmin.site.register(UserFav, UserFavAdmin)

