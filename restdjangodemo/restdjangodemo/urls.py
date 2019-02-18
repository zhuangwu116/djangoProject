"""restdjangodemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve

from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

import xadmin

from users.views import SmsCodeViewset, UserViewset
from goods.views import GoodsListViewSet, CategoryViewSet, HotSearchsViewset
from user_operation.views import UserFaviewset, LeavingMessageViewset


router = DefaultRouter()

router.register(r'goods', GoodsListViewSet, base_name='goods')

router.register(r'categorys', CategoryViewSet, base_name='categorys')

router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")

router.register(r'codes', SmsCodeViewset, base_name='codes')

router.register(r'users', UserViewset, base_name='users')

router.register(r'userfavs', UserFaviewset, base_name='userfavs')

router.register(r'messages', LeavingMessageViewset, base_name='messages')
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
# })

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^login/', obtain_jwt_token),
    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'docs/', include_docs_urls(title="慕学生鲜")),
    url(
        r'^(?P<version>(v1|v2))/',
        include(router.urls),
    )
]
