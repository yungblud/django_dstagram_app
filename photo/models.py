from django.contrib.auth.models import User
from django.db import models

# Create your models here.

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

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('photo:post_detail', args=[str(self.id)])