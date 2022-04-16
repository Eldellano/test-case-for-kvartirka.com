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
            if self.request.data['previous_comment'] == '':  # если ключ пустой
                previous_comment = None
            else:
                previous_comment = self.request.data['previous_comment']
            serializer.save(post_id=self.request.data['post'], text=self.request.data['text'],
                            previous_comment=previous_comment)

        elif self.request.query_params:
            if 'previous_comment' not in self.request.query_params \
                    or self.request.query_params['previous_comment'] == '':  # если ключ пустой или отсутствует
                previous_comment = None
            else:
                previous_comment = self.request.data['previous_comment']
            serializer.save(post_id=self.request.query_params['post'], text=self.request.query_params['text'],
                            previous_comment=previous_comment)
