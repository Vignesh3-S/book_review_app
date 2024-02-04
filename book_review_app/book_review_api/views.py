from .serializers import BookSerializer
from book_review_app.models import User,ApiUser,Book
from rest_framework.views import APIView
from django.utils.http import  urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

class BookApi(APIView):
    def get(self,request,email,token):
        get_token = token
        try:
            dec_email=urlsafe_base64_decode(force_str(email)).decode()
            user = User.objects.get(email=dec_email)
            user=ApiUser.objects.get(user=user.id)    
        except:
            return Response({'error':'Invalid User'},status=status.HTTP_400_BAD_REQUEST)
        tokendate = str(user.date.year)+str(user.date.month)+str(user.date.day)
        time = datetime.now()
        time_str = str(time.year)+str(time.month)+str(time.day)
        if int(time_str)-int(tokendate) > 15:
           return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)
        if user.token == get_token:
            data = Book.objects.all()
            serializer = BookSerializer(data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)