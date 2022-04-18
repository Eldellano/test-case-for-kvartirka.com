from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('comment/', views.CommentList.as_view()),
    path('all_comment/<int:pk>/', views.AllComment.as_view()),
    path('third_comment/<int:pk>', views.ThirdComment.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
