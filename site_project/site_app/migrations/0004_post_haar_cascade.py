# Generated by Django 5.1 on 2024-08-25 10:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_app', '0003_remove_post_image_post_recognize_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='haar_cascade',
            field=models.FileField(null=True, upload_to='haar_cascades', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xml'])], verbose_name='Распознанное изображение'),
        ),
    ]
