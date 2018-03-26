from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.

# View,,
# Class,
# Function 매개변수로 무조건 (request)
# 용도차이 없음..
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from tagging.views import TaggedObjectList

from photo.models import Photo
# delete후에 (post)
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.contrib import messages

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
    fields = ['title', 'text', 'photo', 'tag']
    template_name = 'photo/upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id

        if form.is_valid():
            form.instance.save()


            # return redirect('/')
            # return self.get_absolute_url(self)
            from django.urls import reverse
            return redirect(reverse("photo:post_detail", kwargs={'pk': form.instance.id}))
        else:
            return self.render_to_response({'form': form})

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/'

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "You do not have permission for deleting this photo")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(DeleteView, self).get(request, *args, **kwargs)

# 파일 과 함께 삭제
@receiver(post_delete, sender=Photo)
def post_delete(sender, instance, **kwargs):
    storage, path = instance.photo.storage, instance.photo.path
    #  디렉터리 보안 관련 사항
    if(path != '.') and (path != 'photos/') and (path != 'photos/.'):
        storage.delete(path)

class UpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['title', 'photo', 'text', 'tag']
    template_name = 'photo/upload.html'

    def get_success_url(self):
        from django.urls import reverse
        return reverse("photo:post_detail", kwargs={'pk': self.object.id})
#     return resolve_url(self.object)


class TagPostList(TaggedObjectList):
    model = Photo
    template_name = 'photo/tagging_post_list.html'

class TagView(TemplateView):
    template_name = 'photo/tagging_list.html'