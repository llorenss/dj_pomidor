from django.test import TestCase
from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1=Book.objects.create(name="testbook10", price=25, author_name='a')
        book_2=Book.objects.create(name="testbook11", price=55, author_name='b')
        data=BooksSerializer([book_1,book_2],many=True).data
        excepted_data = [
               {
            'id':book_1.id,
            'name':'testbook10',
            'price':'25.00',
            'author_name':'a',
            },
              {
            'id':book_2.id,
            'name':'testbook11',
            'price':'55.00',
            'author_name':'b',
            },
           
        ]
        self.assertEqual(excepted_data,data)