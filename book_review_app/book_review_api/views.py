from .serializers import BookSerializer
from book_review_app.models import User,ApiUser,Book,Feedback
from rest_framework.views import APIView
from django.utils.http import  urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.response import Response
from rest_framework import status

class BookApiList(APIView):
    def get(self,request,email,token):
        get_token = token
        try:
            dec_email=urlsafe_base64_decode(force_str(email)).decode()
            user = User.objects.get(email=dec_email)
            user=ApiUser.objects.get(user=user.id)    
        except:
            return Response({"error":'Invalid User'},status=status.HTTP_404_NOT_FOUND)
        if user.token == get_token:
            data = Book.objects.all()
            serializer = BookSerializer(data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request,email,token):
        get_token = token
        try:
            dec_email=urlsafe_base64_decode(force_str(email)).decode()
            user = User.objects.get(email=dec_email)
            user=ApiUser.objects.get(user=user.id)    
        except:
            return Response({'error':'Invalid User'},status=status.HTTP_400_BAD_REQUEST)
        
        if user.token == get_token:
            query = request.POST['search']
            if Book.objects.filter(bookname__icontains = query):
                name = Book.objects.filter(bookname__icontains = query)
            elif Book.objects.filter(bookauthor__icontains = query):
                name = Book.objects.filter(bookauthor__icontains = query)
            elif Book.objects.filter(booktype__icontains = query):
                name = Book.objects.filter(booktype__icontains = query)
            else:
                return Response({'error':'Invalid search'},status=status.HTTP_404_NOT_FOUND)
            
            serializer = BookSerializer(name,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)

class BookApiOne(APIView):
    def get(self,request,email,token,id):
        get_token = token
        try:
            dec_email=urlsafe_base64_decode(force_str(email)).decode()
            user = User.objects.get(email=dec_email)
            user=ApiUser.objects.get(user=user.id)    
        except:
            return Response({'error':'Invalid User'},status=status.HTTP_404_NOT_FOUND)
        if user.token == get_token:
            data = Book.objects.get(id=id)
            serializer = BookSerializer(data)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST) 
          
