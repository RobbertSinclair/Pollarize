# Generated by Django 3.0.7 on 2021-03-12 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll_app', '0002_auto_20210312_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profileImage',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]