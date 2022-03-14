import csv
from os import path
from shutil import copytree, ignore_patterns, rmtree

from django.core.management.base import BaseCommand

from seedlings.models import Category, Seedling


class Command(BaseCommand):
    help = 'Загрузка данных в БД'

    def handle(self, *args, **options):

        with open('../../data/loading_data/Category/Category_data.csv') as file:
            file_data = csv.reader(file, delimiter=';')
            for item in file_data:
                id, name, image, slug = item
                Category.objects.get_or_create(
                    pk=id, title=name, image=image, slug=slug
                )
        with open('../../data/loading_data/Seedlings/Seedlings_data.csv') as file:
            file_data = csv.reader(file, delimiter=';')
            for item in file_data:
                (
                    id, name, category, slug, image, short_desc,
                    full_desc, retail, wholesale, stock
                ) = item
                category_obj = Category.objects.get(title=category)
                Seedling.objects.get_or_create(
                    pk=id, title=name, category=category_obj, image=image,
                    slug=slug, short_description=short_desc,
                    full_description=full_desc, retail_price=retail,
                    wholesale_price=wholesale, stock=stock
                )

        if path.exists('./media'):
            rmtree('./media')
        copytree(
            '../../data/loading_data', './media/',
            ignore=ignore_patterns('*.csv',)
        )
