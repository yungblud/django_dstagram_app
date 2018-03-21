from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# 업로드된 컨텐트 다시 조작
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

class Photo(models.Model):
    # db -> orm..으로 접근(다이렉트가 아닌) ->
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_posts')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=False, null=False, default='photos/no_image.png')
    title = models.CharField(max_length=100, null=False, blank=False, default="Default Title")
    text = models.TextField()

    # time
    # servertime vs 장고 설정 시간
    created = models.DateTimeField(auto_now_add=True)
    # 생성된 처음 시점만..
    updated = models.DateTimeField(auto_now=True)
    # 갱신이 있을때마다(실제 모델이 업데이트될때)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    # *args 파라미터 아무거나
    # **kwargs key와 함께. (딕셔너리) key with arguments
    def save(self, *args, **kwargs):
        is_duplicated = False
        if self.photo:
            try:
                before_obj = Photo.objects.get(id=self.id)
                if before_obj.photo == self.photo:
                    is_duplicated = True
            except:
                pass
        #    업로드된 이미지가 다를때, 즉 수정이 이루어졌을때
        if not is_duplicated:
            # conver("L") : gray-scale로 변경
            image_obj = Image.open(self.photo).convert("L")
            new_image_io = BytesIO()
            image_obj.save(new_image_io, format='JPEG')

            temp_name = self.photo.name
            self.photo.delete(save=False)
            self.photo.save(temp_name, content=ContentFile(new_image_io.getvalue()), save=False)

            try:
                before_obj = Photo.objects.get(id=self.id)
                if before_obj.photo == self.photo or is_duplicated:
                    self.photo = before_obj.photo
                else:
                    before_obj.photo.delete(save=False)
            except:
                pass

            super(Photo, self).save(*args, **kwargs)


    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('photo:post_detail', args=[str(self.id)])