from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.

# View,,
# Class,
# Function 매개변수로 무조건 (request)
# 용도차이 없음..
from django.views.generic import CreateView, DeleteView, UpdateView

from photo.models import Photo

# <로그인 관련 여부 처리>
# 함수형 뷰 : decorator
# 클래스형 뷰 : mixin
# 둘의 용도: 어떤 동작 제어, 권한 설정을 코드로 직접 하는것이 아니라, 장고에 일임..

@login_required
def post_list(request):
    objects = Photo.objects.all()
    return render(request, 'photo/list.html', {'photos': objects})
# Template variable...

class UploadView(LoginRequiredMixin,CreateView):
    model = Photo
    fields = ['title', 'text', 'photo']
    template_name = 'photo/upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/'

class UpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['title', 'photo', 'text']
    template_name = 'photo/upload.html'

