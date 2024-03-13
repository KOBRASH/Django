from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    path('create/', BlogPostCreateView.as_view(), name='create'),
    path('post/<slug:slug>/', BlogPostDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', BlogPostUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='delete'),
]
