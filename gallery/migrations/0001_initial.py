# Generated by Django 4.1.7 on 2023-03-17 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gallery.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery_name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_gallery_user_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ImageGallery',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=gallery.utils.image_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image_gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_gallery_set', to='gallery.imagegallery')),
            ],
            options={
                'db_table': 'Image',
            },
        ),
    ]
