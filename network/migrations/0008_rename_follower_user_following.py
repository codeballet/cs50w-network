# Generated by Django 3.2.7 on 2021-09-21 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_auto_20210919_0153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='follower',
            new_name='following',
        ),
    ]
