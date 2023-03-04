from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from store.models import Book, UserBookRelation


class BooksSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField()

    class Meta:
        model = Book
        # exclude = ["readers"]
        # fields = '__all__'
        fields = (
            "id",
            "name",
            "price",
            "author_name",
            "likes_count",
            "annotated_likes",
        )

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(
            book=instance, like=True
        ).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ("book", "like", "in_bookmarks", "rate")
