# Generated by Django 3.0.7 on 2020-06-23 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='publisher_id',
            new_name='publisher',
        ),
    ]
