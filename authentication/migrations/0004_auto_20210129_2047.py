# Generated by Django 3.1.3 on 2021-01-29 12:47

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_user_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(default='profiles/default_zycnhz.jpg', upload_to='profiles'),
        ),
    ]
