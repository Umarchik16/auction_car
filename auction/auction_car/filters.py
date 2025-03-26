import django_filters
from .models import Car, Auction


class CarFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='brand__brand_name', lookup_expr='iexact')
    model = django_filters.CharFilter(field_name='model__model_name', lookup_expr='icontains')
    year = django_filters.NumberFilter()
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
    fuel_type = django_filters.ChoiceFilter(field_name="fuel_type", choices=Car.FUEL_CHOICES)
    transmission = django_filters.ChoiceFilter(field_name="transmission", choices=Car.AUTO_CHOICES)
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    mileage_min = django_filters.NumberFilter(field_name='mileage', lookup_expr='gte')
    mileage_max = django_filters.NumberFilter(field_name='mileage', lookup_expr='lte')
    auction_status = django_filters.ChoiceFilter(field_name='auction__status', choices=Auction.STATUS_CHOICES)

    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'fuel_type', 'transmission', 'price_min', 'price_max', 'mileage_min', 'mileage_max', 'auction_status']
