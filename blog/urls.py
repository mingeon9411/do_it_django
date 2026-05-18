from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('create/', views.post_create),
    path('category/<str:slug>/', views.PostListByCategory.as_view()),
    path('tag/<str:slug>/', views.PostListByTag.as_view()),
]
