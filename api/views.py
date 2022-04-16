from rest_framework import generics
from . import serializers
from .models import Post, Comment
from django.views.decorators.csrf import csrf_exempt

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    #@csrf_exempt
    def perform_create(self, serializer):
        if self.request.data:  # для вызова из web морды
            serializer.save(title=self.request.data['title'], text=self.request.data['text'])
        elif self.request.query_params:  # для вызова из postman, etc
            serializer.save(title=self.request.query_params['title'], text=self.request.query_params['text'])


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        if self.request.data:
            serializer.save(post_id=self.request.data['post'], text=self.request.data['text'])
        elif self.request.query_params:
            serializer.save(post_id=self.request.query_params['post'], text=self.request.query_params['text'])
