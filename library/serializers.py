from rest_framework import serializers

from library.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def to_representation(self, instance):
        """Enforce `null` if `cover` URLField is empty"""
        representation = super().to_representation(instance)
        if representation.get("cover") == "":
            representation["cover"] = None
        return representation
