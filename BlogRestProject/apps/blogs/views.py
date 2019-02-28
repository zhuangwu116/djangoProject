
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import BlogsArticle
from .filters import BlogsArticleFilter
from .serializers import BlogsTagSerializer, BlogsCategorySerializer, BlogsArticleSerializer, BlogsCommentSerializer
# Create your views here.


class ArticlesPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class BlogsArticleListViewset(CacheResponseMixin, mixins.ListModelMixin,
                              mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = BlogsArticleSerializer
    pagination_class = ArticlesPagination
    queryset = BlogsArticle.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BlogsArticleFilter
    search_fields = ('title', 'user__username')
    ordering_fields = ('click_count', )