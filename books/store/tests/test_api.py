import json
from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer
from rest_framework import status
from django.contrib.auth.models import User


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
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

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {    
            "name":"Py 4",
            "price":1894,
            "author_name":"Teddy"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, json_data,content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
    
    def test_update(self):
        url = reverse('book-detail',args=(self.book_1.id,))
        data = {    
            "name":self.book_1.name,
            "price":575,
            "author_name":self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, json_data,content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)



