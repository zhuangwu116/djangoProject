from django.db.models import Count


from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from django_filters.rest_framework import DjangoFilterBackend

from .models import BlogsArticle, BlogsCategory, BlogsComment
from .filters import BlogsArticleFilter
from .serializers import BlogsCategorySerializer, BlogsArticleSerializer
# Create your views here.


class ArticlesPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class BlogsCategoryListViewset(CacheResponseMixin, mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    serializer_class = BlogsCategorySerializer
    queryset = BlogsCategory.objects.all().order_by('index')

class BlogsArticleListViewset(CacheResponseMixin, mixins.ListModelMixin,
                              mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = BlogsArticleSerializer
    pagination_class = ArticlesPagination
    queryset = BlogsArticle.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BlogsArticleFilter
    search_fields = ('title', 'user__username')
    ordering_fields = ('click_count', 'date_publish')

class BlogsArticleGlobalViewsetBase(mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = BlogsArticleSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        comment_count_list = BlogsComment.objects.values('article').annotate(comment_count=Count('article')).order_by(
            '-comment_count')[:10]

        return comment_count_list

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        article_comment_list = [BlogsArticle.objects.get(pk=comment['article']) for comment in queryset]
        page = self.paginate_queryset(article_comment_list)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(article_comment_list, many=True)
        return Response(serializer.data)



class BlogsArticleGlobalViewset(CacheResponseMixin, BlogsArticleGlobalViewsetBase):
    pass

