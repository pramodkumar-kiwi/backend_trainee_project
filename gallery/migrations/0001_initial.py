# Generated by Django 4.1.7 on 2023-03-15 09:56

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
            name='VideoGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery_name', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_gallery_user_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'VideoGallery',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(null=True, upload_to=gallery.utils.video_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('video_gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_gallery_set', to='gallery.videogallery')),
            ],
            options={
                'db_table': 'Video',
            },
        ),
    ]
