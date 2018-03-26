from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import DetailView

from photo.models import Photo
from photo.views import post_list, UploadView, DeleteView, UpdateView, TagView, TagPostList

app_name = 'photo'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('upload/', UploadView.as_view(), name='photo_upload'),
    path('detail/<int:pk>/', login_required(DetailView.as_view(model=Photo, template_name='photo/detail.html')), name='post_detail'),
    path('delete/<int:pk>/', DeleteView.as_view(), name='photo_delete'),
    path('update/<int:pk>/', UpdateView.as_view(), name='photo_update'),
    path('tag/', TagView.as_view(), name='tag_list'),
    path('tag/<tag>/', TagPostList.as_view(), name='tag_post_list'),
]