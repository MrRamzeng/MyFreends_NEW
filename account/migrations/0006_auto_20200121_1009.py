# Generated by Django 2.2.3 on 2020-01-21 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200121_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(default='j9BaUCj', max_length=20, unique=True),
        ),
    ]
