# Generated by Django 4.0 on 2022-01-02 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_post_comments_allowed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='views',
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clicks', models.PositiveIntegerField(default=0, editable=False, verbose_name='Clicks')),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='core.post', verbose_name='Post')),
            ],
            options={
                'verbose_name': 'View',
                'verbose_name_plural': 'Views',
            },
        ),
    ]
