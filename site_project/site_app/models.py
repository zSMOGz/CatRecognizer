from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Post(models.Model):
    title = models.CharField(verbose_name="Заголовок поста",
                             max_length=100,
                             null=False)
    content = models.TextField(verbose_name="Текст",
                               null=False)
    upload_image = models.ImageField(verbose_name="Изображение для распознавания",
                                     default="default.png",
                                     upload_to="upload_images",
                                     null=False)
    recognize_image = models.ImageField(verbose_name="Распознанное изображение",
                                        upload_to="recognize_images",
                                        null=True)
    date_posted = models.DateTimeField(default=timezone.now,
                                       null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',
                       kwargs={'pk': self.pk})

    def save(self,
             *args,
             **kwargs):
        super(Post, self).save(*args,
                               **kwargs)

        img = Image.open(self.upload_image.path)
        size = 500, 500

        if (img.height > size[0]
                or img.width > size[1]):
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(self.upload_image.path)
