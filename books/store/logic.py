from store.models import UserBookRelation
from django.db.models import Count, Case, When, Avg


def set_rating(book):
    rating = (
        UserBookRelation.objects.filter(book=book)
        .aggregate(rating=Avg("rate"))
        .get("rating")
    )
    book.rating = rating
    book.save()