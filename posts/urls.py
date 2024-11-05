from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='posts-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<str:slug>/comment/', views.add_comment, name='add-comment'),
    path('post/<str:slug>/comment/<uuid:parent_id>/reply/', views.add_comment, name='reply-comment'),
    path('comment/<uuid:comment_id>/edit/', views.edit_comment, name='edit-comment'),
    path('comment/<uuid:comment_id>/delete/', views.delete_comment, name='delete-comment'),
]
