from django.test import TestCase
from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1=Book.objects.create(name="testbook10", price=25)
        book_2=Book.objects.create(name="testbook11", price=55)
        data=BooksSerializer([book_2,book_1],many=True).data
        excepted_data = [
              {
            'id':book_2.id,
            'name':'testbook11',
            'price':'55.00'
            },
            {
            'id':book_1.id,
            'name':'testbook10',
            'price':'25.00'
            },
           
        ]
        self.assertEqual(excepted_data,data)