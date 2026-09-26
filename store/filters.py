import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category__id')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    price = django_filters.NumberFilter(field_name='price', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'price']
