from rest_framework import generics
from . import serializers
from .models import Post
from django.views.decorators.csrf import csrf_exempt

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    #@csrf_exempt
    def perform_create(self, serializer):
        serializer.save(title=self.request.query_params['title'], text=self.request.query_params['text'])


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
