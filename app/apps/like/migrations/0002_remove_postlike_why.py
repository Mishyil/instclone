# Generated by Django 4.2.6 on 2023-11-16 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('like', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postlike',
            name='why',
        ),
    ]
