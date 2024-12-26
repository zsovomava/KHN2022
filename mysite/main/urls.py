from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.home, name='home'),
    path('faq/', TemplateView.as_view(template_name='main/faq.html'), name='faq'),
    path('about', TemplateView.as_view(template_name='main/about.html'), name='about'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/user/<str:username>',
         views.UserPostListView.as_view(), name='user-post-list'),
    path('posts/topic/<str:topic>',
         views.TopicPostListView.as_view(), name='topic-post-list'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.comment, name='post-comment'),
    path('comment/<int:pk>/update/',
         views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/',
         views.CommentDeleteView.as_view(), name='comment-delete'),
    path('videochat/', views.videochat, name='videochat'),
    path('jitsi/<str:room>', views.jitsi, name='jitsi'),
    path('privacy/', TemplateView.as_view(template_name='main/privacy.html'), name='privacy'),
]
