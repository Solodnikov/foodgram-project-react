import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


def get_reader(file_name: str):
    csv_path = os.path.join(settings.BASE_DIR, '../data/', file_name)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    reader = csv.reader(csv_file, delimiter=',')
    return reader


class Command(BaseCommand):

    def handle(self, *args, **options):
        csv_reader = get_reader('ingredients.csv')
        next(csv_reader, None)
        number = 0
        load_count = 0
        for row in csv_reader:
            number += 1
            if Ingredient.objects.filter(
                name=row[0],
                measurement_unit=row[1]
            ).exists():
                print(f'{number}) Ингредиент "{row[0].capitalize()}" '
                      f'с мерой измерения "{row[1]}" '
                      f'уже имеется в базе данных.')
                continue
            else:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
                load_count += 1
                print(f'{number}) Ингредиент "{row[0].capitalize()}" '
                      f'с мерой измерения "{row[1]}" '
                      f'помещен в базу данных.')

        ingredients_count = Ingredient.objects.all().count()
        print(f'Загрузка данных из ingredients.csv завершена.'
              f' Загружено ингредиентов - {load_count}.'
              f' Всего в базе данных {ingredients_count}'
              f' записей ингредиентов.')
