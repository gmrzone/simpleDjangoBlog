# Generated by Django 3.1 on 2020-09-12 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_auto_20200912_0500'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='subtitle',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
