# Generated by Django 4.2.7 on 2023-11-22 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0002_alter_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]
