from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from library.models import Book
from library.serializers import BookSerializer

BOOK_URL = reverse("library:book-list")
BOOK_PAYLOAD = {
    "title": "Sample Book",
    "author": "Sample Author",
    "published_date": "2020-05-22",
    "isbn": "1234567890123",
    "pages": 420,
    "cover": "https://sample.com/cover.jpg",
    "language": "English",
}


def detail_url(book_id: int) -> str:
    return reverse("library:book-detail", args=[book_id])


class GetBookTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.books_data = [
            {
                "title": "The Anarchist Cookbook",
                "author": "William Powell",
                "published_date": "1971-01-01",
                "isbn": "1000000000001",
                "pages": 160,
                "cover": "https://sample.com/cookbook.jpg",
                "language": "English",
            },
            {
                "title": "TiHKAL",
                "author": "Alexander Shulgin",
                "published_date": "1997-06-06",
                "isbn": "1000000000002",
                "pages": 804,
                "cover": "https://sample.com/thikal.jpg",
                "language": "English",
            },
            {
                "title": "Bardo Thodol",
                "author": "Karma Lingpa",
                "published_date": "1971-08-18",
                "isbn": "1000000000003",
                "pages": 404,
                "cover": "https://sample.com/bardo.jpg",
                "language": "Indian",
            },
            {
                "title": "PiHKAL",
                "author": "Alexander Shulgin",
                "published_date": "1971-02-22",
                "isbn": "1000000000004",
                "pages": 978,
                "cover": "https://sample.com/phikal.jpg",
                "language": "English",
            },
            {
                "title": "Federalist papers",
                "author": "Alexander Hamilton",
                "isbn": "1000000000005",
                "language": "Indian",
            },
        ]
        cls.books = [Book(**book_data) for book_data in cls.books_data]
        Book.objects.bulk_create(cls.books)

    def assertBooksListEqual(self, response, expected_data):
        serializer = BookSerializer(expected_data, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_list_books_without_filters(self):
        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        self.assertBooksListEqual(res, books)

    def test_list_books_with_author_filter(self):
        res = self.client.get(BOOK_URL, {"author": "William Powell"})
        books = Book.objects.filter(author__icontains="William Powell")
        self.assertBooksListEqual(res, books)

    def test_list_books_with_date_filter(self):
        res = self.client.get(BOOK_URL, {"published_year": "1997"})
        books = Book.objects.filter(published_date__year=1997)
        self.assertBooksListEqual(res, books)

    def test_list_books_with_language_filter(self):
        res = self.client.get(BOOK_URL, {"language": "Indian"})
        books = Book.objects.filter(language__icontains="Indian")
        self.assertBooksListEqual(res, books)

    def test_list_books_with_combined_filters(self):
        res = self.client.get(
            BOOK_URL,
            {
                "author": "alexander",
                "published_year": "1971",
                "language": "english",
            },
        )
        books = Book.objects.filter(
            published_date__year=1971,
            language__icontains="english",
            author__icontains="alexander",
        )
        self.assertBooksListEqual(res, books)

    def test_retrieve_book(self):
        book = Book.objects.get(isbn="1000000000001")
        serializer = BookSerializer(book)

        res = self.client.get(detail_url(book.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book_with_partial_data(self):
        book = Book.objects.get(isbn="1000000000005")
        serializer = BookSerializer(book)

        res = self.client.get(detail_url(book.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    @classmethod
    def tearDownClass(cls):
        Book.objects.all().delete()
        super().tearDownClass()


class PostPutDeleteBookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="The Anarchist Cookbook",
            author="William Powell",
            published_date="1971-01-01",
            isbn="1000000000001",
            pages=160,
            cover="https://sample.com/cookbook.jpg",
            language="English",
        )

    def assertBookEqual(self, payload: dict, expected_data: Book):
        serializer = BookSerializer(expected_data)
        for key in payload.keys():
            self.assertEqual(serializer.data[key], payload[key])

    def test_create_book(self):
        res = self.client.post(BOOK_URL, BOOK_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(isbn=BOOK_PAYLOAD["isbn"])
        self.assertBookEqual(BOOK_PAYLOAD, book)

    def test_create_book_with_partial_data(self):
        partial_payload = {
            "title": "Partial Book",
            "author": "Partial Author",
            "isbn": "123456790123",
            "language": "English",
        }

        res = self.client.post(BOOK_URL, partial_payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        partial_payload.update(
            {
                "published_date": None,
                "pages": None,
                "cover": None,
            }
        )
        book = Book.objects.get(isbn=partial_payload["isbn"])
        self.assertBookEqual(partial_payload, book)

    def test_cannot_create_book_with_same_isbn(self):
        book_payload = {
            "title": "Sample Book",
            "author": "Sample Author",
            "published_date": "2020-05-22",
            "isbn": "1000000000001",
            "pages": 420,
            "cover": "https://sample.com/cover.jpg",
            "language": "English",
        }
        res = self.client.post(BOOK_URL, book_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book(self):
        url = detail_url(self.book.id)
        res = self.client.put(url, BOOK_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        book = Book.objects.first()
        self.assertBookEqual(BOOK_PAYLOAD, book)

    def test_delete_book(self):
        res = self.client.delete(detail_url(self.book.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        books = Book.objects.all()
        self.assertEqual(len(books), 0)
