# Generated by Django 3.0.7 on 2021-03-13 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll_app', '0006_auto_20210313_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profileImage',
            field=models.ImageField(null=True, upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
