from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Goods

###http://127.0.0.1:8000/api/v1/goods/?min_price=&max_price=&top_category=1
class GoodsFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(field_name="shop_price", help_text='最低价格', lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    top_category = filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id = value) |
                                   Q(category__parent_category_id = value) |
                                   Q(category__parent_category__parent_category_id = value))
    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']