# Generated by Django 3.1 on 2020-09-17 10:39

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('myblog', '0010_auto_20200916_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tag',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]