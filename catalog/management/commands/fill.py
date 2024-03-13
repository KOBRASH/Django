from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()  # Очистка данных

        # Пытаемся получить категорию 'Напитки'; если она не существует, создаем ее
        category, created = Category.objects.get_or_create(name='Напитки')

        # Создаем объекты Product только если категория успешно получена или создана
        if created or category:
            Product.objects.create(name='Кола', description='Вкус детства!', category=category, price=5.9)
            Product.objects.create(name='Сок', description='Добрый как Мама!', category=category, price=2.49)
        else:
            self.stdout.write(self.style.WARNING('Категория "Напитки" уже существует. Пропущено создание.'))

