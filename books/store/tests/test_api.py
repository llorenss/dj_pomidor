from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer
from rest_framework import status

class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.book_1=Book.objects.create(name="testbook10", price=25, author_name='a klod')
        self.book_2=Book.objects.create(name="testbook11", price=55, author_name='add')
        self.book_3=Book.objects.create(name="testbook12 klod", price=55, author_name='c')


    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data=BooksSerializer([self.book_1,self.book_2,self.book_3],many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data,response.data)
    
    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search':'klod'})
        serializer_data=BooksSerializer([self.book_1,self.book_3],many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data,response.data)

