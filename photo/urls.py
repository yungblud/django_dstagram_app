from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import DetailView

from photo.models import Photo
from photo.views import post_list, UploadView

app_name = 'photo'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('upload/', UploadView.as_view(), name='photo_upload'),
    path('detail/<int:pk>/', login_required(DetailView.as_view(model=Photo, template_name='photo/detail.html')), name='post_detail'),
]