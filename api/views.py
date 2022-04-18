from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .models import Post, Comment


class PostList(generics.ListCreateAPIView):
    """Получение и создание Статей"""
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        if self.request.data:  # для вызова из web морды
            serializer.save(title=self.request.data['title'], text=self.request.data['text'])
        elif self.request.query_params:  # для вызова из postman, etc
            serializer.save(title=self.request.query_params['title'], text=self.request.query_params['text'])


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer


class CommentList(generics.ListCreateAPIView):
    """Получение и создание комментариев для статьи"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        if self.request.data:
            if self.request.data['parent'] == '':  # если ключ пустой
                parent = None
            else:
                parent = Comment.objects.get(id=self.request.data['parent'])
            serializer.save(post_id=self.request.data['post'], text=self.request.data['text'],
                            parent=parent)

        elif self.request.query_params:
            # if 'parent' not in self.request.query_params \
            #         or self.request.query_params['parent'] == '':  # если ключ пустой или отсутствует
            #     parent = None
            # else:
            #     parent = self.request.data['parent']
            serializer.save(post_id=self.request.query_params['post'], text=self.request.query_params['text'],
                            parent=self)


class AllComment(APIView):
    """Получение всех комментариев вложенностью до третьего уровня для статьи (level__lte=2 - отсчет от 0) """
    def get(self, request, pk):
        queryset = Comment.objects.filter(post_id=pk, level__lte=2).order_by('id')
        serializer = serializers.CommentSerializer(queryset, many=True)
        return Response(serializer.data)


class ThirdComment(APIView):
    """Получение всех вложенных комментариев для комментария"""
    def get(self, request, pk):
        third_comment = Comment.objects.get(children=pk)  # объект заданного комментария
        print(third_comment)
        queryset = Comment.objects.filter(level__gt=third_comment.level, post_id=third_comment.post_id)\
            .get_descendants(include_self=True)
        serializer = serializers.CommentSerializer(queryset, many=True)
        return Response(serializer.data)
