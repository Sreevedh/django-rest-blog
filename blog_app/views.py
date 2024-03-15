from django.shortcuts import render


# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator


class PublicView(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')

            if request.GET.get('search'):
                search  = request.GET.get('search')
                blogs = blogs.filter(Q (title__icontains = search) | Q(blog_text__icontains = search))

            #pagination
            paginator = Paginator(blogs, 3) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            serializer = BlogSerializer(page_obj, many=True)



            return Response(
                {
                    'data':serializer.data,
                    'message':'Blogs fetched successfully'
                },
                status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                'data':serializer.data,
                'message':'Something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user = request.user)

            if request.GET.get('search'):
                search  = request.GET.get('search')
                blogs = blogs.filter(Q (title__icontains = search) | Q(blog_text__icontains = search))

            serializer = BlogSerializer(blogs, many=True)

            return Response(
                {
                    'data':serializer.data,
                    'message':'Blogs fetched successfully'
                },
                status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                'data':serializer.data,
                'message':'Something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            serializer = BlogSerializer(data=data)

            data['user'] = request.user.id
            print(request.user)

            # return Response()
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'Invalid data'
                    },status=status.HTTP_400_BAD_REQUEST
                    )
            
            serializer.save()

            return Response(
                {
                    'data':serializer.data,
                    'message':'Blog created successfully'
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            print(e)
            return Response({
                'data':'ASDASDASDA',
                'message':'Internal server error'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self,request):
        try:
            data = request.data
            blog = Blog.objects.get(uid = data['uid'])

            if request.user != blog.user:
                return Response({
                    'data':'',
                    'message':'You are not authorized to update this blog'
                },status=status.HTTP_401_UNAUTHORIZED)
            
            print(data)

            serializer = BlogSerializer(blog, data = data, partial = True)

            if not serializer.is_valid():

                return Response({
                    'data':serializer.data,
                    'message':'Something went wrong'
                },status=status.HTTP_200_OK)
            
            serializer.save()
            
            return Response({
            'data':serializer.data,
            'message':'Blog updated successfully'
        },status=status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return Response({
                'data':'{}',
                'message':'Something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.get(uid = data['uid'])

            if request.user != blog.user:
                return Response({
                    'data':'',
                    'message':'You are not authorized to delete this blog'
                },status=status.HTTP_401_UNAUTHORIZED)
            
            blog.delete()
            return Response({
                'data':'',
                'message':'Blog deleted successfully'
            },status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data':'',
                'message':'Something went wrong'
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)