from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=16, unique=True)
    pages = models.IntegerField(blank=True, null=True)
    cover = models.URLField(max_length=511, blank=True, null=True)
    language = models.CharField(max_length=255)

    class Meta:
        ordering = ["title", "author"]

    def __str__(self):
        return f"{self.title}({self.author})"
