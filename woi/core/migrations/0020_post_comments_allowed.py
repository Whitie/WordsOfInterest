# Generated by Django 4.0 on 2022-01-02 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_extension_js_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments_allowed',
            field=models.BooleanField(default=True, verbose_name='Comments allowed'),
        ),
    ]
