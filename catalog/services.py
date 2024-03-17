from django.core.cache import cache
from .models import Category

def get_categories():
    # Пытаемся получить список категорий из кэша
    categories = cache.get('categories')

    # Если список категорий отсутствует в кэше, делаем запрос к базе данных
    if not categories:
        categories = list(Category.objects.all())

        # Сохраняем список категорий в кэше на 24 часа
        cache.set('categories', categories, timeout=86400)

    return categories
