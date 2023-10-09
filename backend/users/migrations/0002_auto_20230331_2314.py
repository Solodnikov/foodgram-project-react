# Generated by Django 3.2.18 on 2023-03-31 20:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(message='Не бывает имен с цифорками и всякими закорючками, допустимы только буквы.', regex='^[а-яА-Яa-zA-Z ]+\\Z')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(message='Не бывает фамилий с цифорками и всякими закорючками, допустимы только буквы.', regex='^[а-яА-Яa-zA-Z ]+\\Z')], verbose_name='Фамилия'),
        ),
    ]