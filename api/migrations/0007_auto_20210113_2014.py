# Generated by Django 3.0.5 on 2021-01-13 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210112_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, default=models.EmailField(max_length=128, unique=True, verbose_name='Адрес электронной почты'), max_length=30, unique=True, verbose_name='Логин'),
        ),
    ]
