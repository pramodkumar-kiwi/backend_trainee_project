# Generated by Django 4.1.7 on 2023-03-02 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('name', models.CharField(max_length=20)),
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
                ('video', models.FileField(null=True, upload_to='media/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('video_gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_gallery_set', to='video.videogallery')),
            ],
            options={
                'db_table': 'Video',
            },
        ),
    ]
