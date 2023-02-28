from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from store.serializers import BooksSerializer
from store.models import Book

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer

