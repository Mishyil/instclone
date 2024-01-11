# Generated by Django 4.2.6 on 2023-12-07 05:27

from django.db import migrations, models
import userprofile.models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, storage=userprofile.models.AvatarS3Storage(), upload_to=''),
        ),
    ]