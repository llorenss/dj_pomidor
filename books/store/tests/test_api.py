from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer
from rest_framework import status

class BooksApiTestCase(APITestCase):
    def test_get(self):
        book_1=Book.objects.create(name="testbook10", price=25)
        book_2=Book.objects.create(name="testbook11", price=55)
        url = reverse('book-list')
        # print(url)
        response = self.client.get(url)
        serializer_data=BooksSerializer([book_2,book_1],many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data,response.data)
        print(response.data)

