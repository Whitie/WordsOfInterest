# Generated by Django 4.0 on 2021-12-30 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_extension_html_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extension',
            name='html_id',
        ),
    ]
