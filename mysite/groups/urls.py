from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')

app_name = 'groups'
urlpatterns = [
    path('groups/', views.GroupListView.as_view(), name='group-list'),
    path('group/<int:pk>/', views.GroupDetailView.as_view(), name='group-detail'),
    path('group/new/', views.GroupCreateView.as_view(), name='group-create'),
    path('group/<int:pk>/update/',
         views.GroupUpdateView.as_view(), name='group-update'),
    path('group/<int:pk>/delete/',
         views.GroupDeleteView.as_view(), name='group-delete'),
    path('group/<int:pk>/leave/', views.group_leave, name='group-leave'),
    path('group/<int:pk>/join/', views.group_join, name='group-join'),
    path('api/', include(router.urls)),
]
