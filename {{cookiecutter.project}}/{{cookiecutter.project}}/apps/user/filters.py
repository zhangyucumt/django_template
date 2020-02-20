from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model


class UserFilter(filters.FilterSet):
    date_joined__lt = filters.DateTimeFilter(field_name='date_joined', lookup_expr='lt')
    date_joined__gt = filters.DateTimeFilter(field_name='date_joined', lookup_expr='gt')
    # email = filters.CharFilter(field_name='email')
    is_superuser = filters.BooleanFilter(field_name='is_superuser')

    class Meta:
        model = get_user_model()
        fields = {
            'id': ['lt', 'gt']
        }
