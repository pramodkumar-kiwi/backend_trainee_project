# Generated by Django 4.1.7 on 2023-03-16 08:08

from django.db import migrations, models
import gallery.utils


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_alter_video_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(null=True, upload_to=gallery.utils.video_upload_path),
        ),
    ]
