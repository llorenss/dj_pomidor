from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from store.serializers import BooksSerializer, UserBookRelationSerializer
from store.models import Book, UserBookRelation
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from store.permissions import IsOwnerOrStaffOrReadOnly
from rest_framework.mixins import UpdateModelMixin
from django.db.models import Count, Case, When, Avg


class BookViewSet(ModelViewSet):
    # queryset = Book.objects.all()
    queryset = (
        Book.objects.all()
        .annotate(
            annotated_likes=Count(
                Case(When(userbookrelation__like=True, then=1))
            )
        )
        .order_by("id")
    )
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ["price"]
    search_fields = ["name", "author_name"]
    ordering_fields = ["price", "author_name"]

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        serializer.save()


class UserBooksRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = "book"

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(
            user=self.request.user, book_id=self.kwargs["book"]
        )
        # просмотр при тестировании был
        # obj, created = UserBookRelation.objects.get_or_create(user=self.request.user,
        #                                                 book_id=self.kwargs['book'])

        # print('created', created)
        return obj


def auth(request):
    return render(request, "oauth.html")
