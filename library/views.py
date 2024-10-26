from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from library.models import Book
from library.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ["author", "published_date", "language"]
