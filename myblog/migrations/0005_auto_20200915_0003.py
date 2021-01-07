# Generated by Django 3.1 on 2020-09-15 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='num_verified',
            field=models.BooleanField(default=False, verbose_name='Verified'),
        ),
        migrations.AddField(
            model_name='profile',
            name='number',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
