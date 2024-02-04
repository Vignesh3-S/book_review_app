from book_review_app.models import Book
from rest_framework.serializers import ModelSerializer

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        exclude = ['id','user','created_datetime','modified_datetime',]