from django.test import TestCase
from store.models import Book
from store.serializers import BooksSerializer
from django.contrib.auth.models import User


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        self.user_1 = User.objects.create(username='test_username')
        self.user_2 = User.objects.create(username='test_username3')
        book_1=Book.objects.create(name="testbook10", price=25, author_name='a',owner=self.user_1)
        book_2=Book.objects.create(name="testbook11", price=55, author_name='b',owner=self.user_2)
        data=BooksSerializer([book_1,book_2],many=True).data
        excepted_data = [
               {
            'id':book_1.id,
            'name':'testbook10',
            'price':'25.00',
            'author_name':'a',
            'owner': book_1.owner.id 
            },
              {
            'id':book_2.id,
            'name':'testbook11',
            'price':'55.00',
            'author_name':'b',
            'owner': book_2.owner.id 
            },
           
        ]
        self.assertEqual(excepted_data,data)