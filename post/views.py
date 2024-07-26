from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from intelregion.modules.exceptions import raise_serializer_error_msg
from intelregion.modules.permissions import IsBlogOwner, IsCommentAuthor, IsCommentOwner, IsPostAuthor
from intelregion.modules.utils import api_response, get_incoming_request_checks, incoming_request_checks
from post.models import Blog, Comment
from .serializers import BlogDetailSerializer, BlogSerializer, BlogSerializerIn, CommentSerializer, CommentSerializerIn
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.filters import SearchFilter
# from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class BlogView(ModelViewSet):
    """    
        PAYLOAD
    
    {
        "requestType":"inbound",
        "data":{
            "title":"Blog 1",
            "body":"This is the bodyy",
            "category":1,       integer id of a category
            "image":image-file  this is nullable
        }
    }
    
    blog/{id}   == To Get a single news and Update it
    """
    
    # permission_classes = [IsAuthenticated & (IsAdmin | IsAgentAdmin)]
    serializer_class = BlogDetailSerializer
    queryset = Blog.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title']
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = 
    
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return BlogSerializerIn
        return super().get_serializer_class()
    
        
    def get_serializer_context(self):
        return {'user_id' : self.request.user.id}
        
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            # return [IsPostAuthor]
            return [permissions.IsAuthenticated(), IsBlogOwner()]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = self.filter_queryset(self.get_queryset())
        if len(queryset) == 0:
            return Response(
                api_response(
                    message="No blog at the moment", status=True, data=None
                )
            )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BlogSerializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response(
            api_response(
                message="News Retrieved Successfully", status=True, data=response.data
                )
            )

        serializer = BlogSerializer(queryset, many=True)
        response = serializer.data
        return Response(
            api_response(
                message="News Retrieved Successfully", status=True, data=response
            )
        )
        
    def retrieve(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = self.get_object()
        if instance is None:
            return Response(
                api_response(
                    message="The blog you are trying to get is not available", status=True, data=None
                )
            )
        serializer = self.get_serializer(instance)
        return Response(
            api_response(
                message=f"News retrieved Successfully", status=True, data=serializer.data
            )
        )

    def create(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        data['owner'] = self.request.user.id
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        data : dict = data
        title = data.get('title', None)
        if title is not None:
            if Blog.objects.filter(title=title).exists():
                return Response({'message':'Blog with the title already exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = serializer.save()
        return Response(
            api_response(
                message="Blog Created Successfully", status=True, data=response
            )
        )
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = self.get_object()
        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        data : dict = data
        title = data.get('title', None)
        if title is not None:
            if Blog.objects.filter(title=title).exists() and Blog.objects.get(title=title).id != instance.id:
                return Response({'message':'Blog with the title already exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = serializer.save()
        return Response(
            api_response(
                message="Blog Updated Successfully", status=True, data=response
            )
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete
        return Response(api_response(
                        message="Comment Updated Successfully",
                        status=True),
                        status=status.HTTP_204_NO_CONTENT)


class CommentView(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """    
        PAYLOAD
    
    {
        "requestType":"inbound",
        "data":{
            "title":"Blog 1",
            "body":"This is the bodyy",
            "category":1,       integer id of a category
            "image":image-file  this is nullable
        }
    }
    
    news/{id}   == To Get a single news and Update it
    """
    
    # permission_classes = [IsAuthenticated & (IsAdmin | IsAgentAdmin)]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        return {'user_id' : self.request.user.id,
                'blog_id': self.kwargs.get('blog_pk', None)}
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return CommentSerializerIn
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [IsCommentAuthor]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = self.filter_queryset(self.get_queryset())
        if len(queryset) == 0:
            return Response(
                api_response(
                    message="No Comment for the blog at the moment", status=True, data=None
                )
            )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response(
            api_response(
                message="Comments Retrieved Successfully", status=True, data=response.data
                )
            )

        serializer = self.get_serializer(queryset, many=True)
        response = serializer.data
        return Response(
            api_response(
                message="Comments Retrieved Successfully", status=True, data=response
            )
        )
     
    def create(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        
        response = serializer.save()
        return Response(
            api_response(
                message="Comment Created Successfully", status=True, data=response
            )
        )
        return super().create(request, *args, **kwargs)
    
class CommentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return CommentSerializerIn
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsCommentOwner()]

        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = self.get_object()
        if instance is None:
            return Response(
                api_response(
                    message="The comment you are trying to get is not available", status=True, data=None
                )
            )
        serializer = self.get_serializer(instance)
        return Response(
            api_response(
                message=f"comment retrieved Successfully", status=True, data=serializer.data
            )
        )

    def update(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = self.get_object()
        partial = kwargs.pop('partial', True)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        
        response = serializer.save()
        return Response(
            api_response(
                message="Comment Updated Successfully", status=True, data=response
            )
        )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete
        return Response(api_response(message="Comment Deleted Successfully",
                                     status=True),
                        status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
