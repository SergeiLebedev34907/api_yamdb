# Generated by Django 2.2.16 on 2022-01-16 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220117_0110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='title',
            new_name='name',
        ),
    ]
