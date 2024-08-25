import os
import cv2

from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from hashlib import md5

from .cat_recognizer import detect_cat_face
from site_project.settings import MEDIA_ROOT


def get_haar_cascade():
    haar_cascade = []
    haar_cascade_names = ['eye',
                          'eyeglass',
                          'cat',
                          'cat extends',
                          'face alt',
                          'face alt2',
                          'face alt tree',
                          'face default',
                          'full body',
                          'left eye 2splits',
                          'license plate rus 16',
                          'lower body',
                          'profile face',
                          'right eye 2splits',
                          'russian plate number',
                          'smile',
                          'upper body']

    for root, dirs, files in os.walk(cv2.data.haarcascades):
        for file in files:
            if file.endswith(".xml"):
                haar_cascade.append(file)

    return zip(haar_cascade,
               haar_cascade_names)


class Post(models.Model):
    haar_cascade_pairs = get_haar_cascade()

    title = models.CharField(verbose_name="Заголовок поста",
                             max_length=100,
                             null=False)
    content = models.TextField(verbose_name="Текст",
                               null=False)
    haar_cascade = models.CharField(choices=haar_cascade_pairs,
                                    verbose_name="Классификатор",
                                    max_length=100,
                                    null=True)
    upload_image = models.ImageField(verbose_name="Изображение для распознавания",
                                     default="default.png",
                                     upload_to="upload_images",
                                     null=False)
    recognize_image = models.ImageField(verbose_name="Распознанное изображение",
                                        upload_to="recognize_images",
                                        null=True)
    date_posted = models.DateTimeField(default=timezone.now,
                                       null=False)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',
                       kwargs={'pk': self.pk})

    def save(self,
             *args,
             **kwargs):
        if not os.path.isfile(self.upload_image.path):
            super(Post, self).save(*args,
                                   **kwargs)

            img = Image.open(self.upload_image.path)
            size = 1000, 1000

            if (img.height > size[0]
                    or img.width > size[1]
                    or img.height < size[0]
                    or img.height < size[1]):
                img.thumbnail(size, Image.Resampling.LANCZOS)

                img.save(self.upload_image.path)

        haar_cascade_pairs = get_haar_cascade()

        recognize_img = detect_cat_face(self.upload_image,
                                        self.haar_cascade,
                                        list(filter(lambda x: x[0] == self.haar_cascade, haar_cascade_pairs))[0])
        if recognize_img is not None:
            recognize_img_path = MEDIA_ROOT + '\\recognize_images\\'
            recognize_img_name = self.upload_image.name.split("/")[1]
            recognize_img_full_path = os.path.join(recognize_img_path,
                                                   recognize_img_name)

            if not os.path.isfile(recognize_img_full_path):
                recognize_img.save(recognize_img_full_path)

                fs = FileSystemStorage(location=recognize_img_path)
                with open(recognize_img_full_path, 'rb') as f:
                    file = fs.save(recognize_img_name,
                                   f)

                    self.recognize_image.name = os.path.join(recognize_img_path,
                                                             recognize_img_name)

                    self.recognize_image.save(recognize_img_name,
                                              File(f))

                super(Post, self).save(*args,
                                       **kwargs)
        else:
            print("Не удалось распознать картинку")
