from django_filters import rest_framework as filters, RangeFilter

from users.models import User


class UsersProfilesFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    gender = filters.ChoiceFilter(choices=User.GENDER_CHOICES)

    age = filters.NumberFilter(field_name='age', lookup_expr='exact')
    age__qte = filters.NumberFilter(field_name='age', lookup_expr='gte')
    age__lte = filters.NumberFilter(field_name='age', lookup_expr='lte')

    class Meta:
        model = User
        fields = ['username', 'gender', 'age']

