from django_filters import rest_framework as filters

from library.models import Book


class BookFilter(filters.FilterSet):
    author = filters.CharFilter(field_name="author", lookup_expr="icontains")
    language = filters.CharFilter(
        field_name="language", lookup_expr="icontains"
    )
    published_year = filters.NumberFilter(
        field_name="published_date", lookup_expr="year"
    )

    class Meta:
        model = Book
        fields = ["author", "language", "published_year"]
