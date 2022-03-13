import csv
from os import path
from shutil import copytree, ignore_patterns, rmtree

from django.core.management.base import BaseCommand
from seedlings.models import Category, Seedling


class Command(BaseCommand):
    help = 'Выгрузка данных из БД'

    def handle(self, *args, **options):
        pass
