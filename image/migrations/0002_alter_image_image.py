# Generated by Django 4.1.7 on 2023-03-13 08:59

from django.db import migrations, models
import image.utils


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=image.utils.image_upload_path),
        ),
    ]
