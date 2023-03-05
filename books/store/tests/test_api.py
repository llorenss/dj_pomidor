import json
from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.exceptions import ErrorDetail
from django.db.models import Count, Case, When, Avg


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_username",
        )
        self.book_1 = Book.objects.create(
            name="testbook10",
            price=25,
            author_name="Author 1",
            owner=self.user,
        )
        self.book_2 = Book.objects.create(
            name="testbook11", price=55, author_name="add"
        )
        self.book_3 = Book.objects.create(
            name="testbook12 klod", price=55, author_name="c"
        )

    def test_get(self):
        url = reverse("book-list")
        response = self.client.get(url)
        books = (
            Book.objects.all()
            .annotate(
                annotated_likes=Count(
                    Case(When(userbookrelation__like=True, then=1))
                ),
                rating=Avg("userbookrelation__rate"),
            )
            .order_by("id")
        )
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse("book-list")
        books = (
            Book.objects.filter(id__in=[self.book_2.id, self.book_3.id])
            .annotate(
                annotated_likes=Count(
                    Case(When(userbookrelation__like=True, then=1))
                ),
                rating=Avg("userbookrelation__rate"),
            )
            .order_by("id")
        )
        response = self.client.get(url, data={"price": 55})
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse("book-list")
        books = (
            Book.objects.filter(id__in=[self.book_1.id, self.book_3.id])
            .annotate(
                annotated_likes=Count(
                    Case(When(userbookrelation__like=True, then=1))
                ),
                rating=Avg("userbookrelation__rate"),
            )
            .order_by("id")
        )
        response = self.client.get(url, data={"search": "Author 1"})
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse("book-list")
        data = {"name": "Py 4", "price": 1894, "author_name": "Teddy"}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(
            url, json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(
            url, json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

    def test_update_not_owner(self):
        self.user2 = User.objects.create(
            username="test_username2",
        )
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(
            url, json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(
            {
                "detail": ErrorDetail(
                    string="You do not have permission to perform this action.",
                    code="permission_denied",
                )
            },
            response.data,
        )
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(25, self.book_1.price)

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(
            username="test_username2", is_staff=True
        )
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_username",
        )
        self.user2 = User.objects.create(
            username="test_username2",
        )
        self.book_1 = Book.objects.create(
            name="testbook10", price=25, author_name="a klod", owner=self.user
        )
        self.book_2 = Book.objects.create(
            name="testbook11", price=55, author_name="add"
        )
        self.book_3 = Book.objects.create(
            name="testbook12 klod", price=55, author_name="c"
        )

    def test_like(self):
        url = reverse("userbookrelation-detail", args=(self.book_1.id,))
        data = {
            "like": True,
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(
            user=self.user, book=self.book_1
        )
        self.assertTrue(relation.like)

        data = {
            "in_bookmarks": True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(
            user=self.user, book=self.book_1
        )
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse("userbookrelation-detail", args=(self.book_1.id,))
        data = {
            "rate": 3,
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(
            user=self.user, book=self.book_1
        )
        self.assertEqual(3, relation.rate)

    def test_rate_wrong(self):
        url = reverse("userbookrelation-detail", args=(self.book_1.id,))
        data = {
            "rate": 6,
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.patch(
            url, data=json_data, content_type="application/json"
        )
        self.assertEqual(
            status.HTTP_400_BAD_REQUEST, response.status_code, response.data
        )
