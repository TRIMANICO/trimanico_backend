# Generated by Django 5.0.6 on 2024-06-13 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
    ]
