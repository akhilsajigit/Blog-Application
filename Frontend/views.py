from django.shortcuts import render, redirect
from rest_framework.response import Response

from Frontend.serializers import *
from django.views.decorators.csrf import csrf_exempt
from Frontend.models import *
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.views import APIView
from Frontend.serializers import BlogUserSerializer
from Frontend.serializers import PostSerializer

from rest_framework.generics import ListAPIView

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import logout

from rest_framework.pagination import PageNumberPagination


# Pagination size fixing
class Pagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


# Getting user data
class PostModalView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# User creation 

class BlogUserCreateView(APIView):
    http_method_names = ['post']
    serializer_class = BlogUserSerializer
    def post(self, request, *args, **kwargs):
        blog_user_data = request.data
        blog_user_serializer = self.serializer_class(data=blog_user_data)
        if blog_user_serializer.is_valid():
            blog_user_serializer.save()
            return Response({'message':'user created successfully'},status=201)
        else:
            return Response(blog_user_serializer.errors,status=400)

# Creating login token for user
class LoginView(APIView):
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'message':'Crudentials invalid'},status=400)
        else:
            refresh_token = RefreshToken.for_user(user)
            return Response ({'refresh_token':str(refresh_token),'access_token':str(refresh_token.access_token)},status=200)
        
    # Logout sesssion for user
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'message':'Logout successfully'})


    # Updating Post
class BlogUSerRetrieveUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','put']
    serializer_class = BlogUserSerializer
    def get(self, request, *args, **kwargs):
        user = request.user
        blog_user_serializer = self.serializer_class(user)
        return Response(blog_user_serializer.data,status=200)
    def put(self, request, *args, **kwargs):
        user = request.user
        blog_user_data = request.data
        blog_user_serializer = self.serializer_class(user,data=blog_user_data,partial=True)
        if blog_user_serializer.is_valid():
            blog_user_serializer.save()
            return Response({'message':'user updated successfully'},status=200)

 

# Getting post data from user
class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    serializer_class = PostSerializer
    def post(self, request, *args, **kwargs):
        user= request.user
        post_data = request.data
        post_serializer = self.serializer_class(data=post_data)
        if post_serializer.is_valid():
            post_serializer.save(user=user)
            return Response({'message':'post created successfully'},status=201)
        else:
            return Response(post_serializer.errors,status=400)



# Post Updation
class PostRetreiveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','put','delete']
    serializer_class = PostSerializer
    def get_obj(self,request, kwargs):
        try:
            id = kwargs.get('id')
            user = request.user
            return Post.objects.get(id=id, user=user)
        except Post.DoesNotExist :
            return Post.objects.none()

    def get(self, request, *args, **kwargs):
        
        post = self.get_obj(request, kwargs)
        post_serializer = self.serializer_class(post)
        return Response(post_serializer.data,status=200)
        
    def put(self, request, *args, **kwargs):
        post = self.get_obj(request,kwargs)
        post_data = request.data
        post_serializer = self.serializer_class(post,data=post_data, partial=True)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response({'message':'post updated successfully'},status=200)
        else:
            return Response(post_serializer.errors,status=400)

    def delete(self, request, *args, **kwargs):
        post = self.get_obj(request, kwargs)
        post.delete()
        return Response({'message':'Post deleted successfully '},status=200)    
    

    # User List View
class UserPostListView(ListAPIView):  
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    pagination_class = Pagination
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user)

  # User List all post view
class PostListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    pagination_class = Pagination
    serializer_class = PostSerializer
    queryset = Post.objects.all()