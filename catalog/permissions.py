# permissions.py

from django.contrib.auth.models import Group, Permission

# Создаем группу для модератора
moderator_group, created = Group.objects.get_or_create(name='Модератор')

# Получаем или создаем разрешения для модераторов
can_cancel_product_publication, created = Permission.objects.get_or_create(codename='can_cancel_product_publication', name='Может отменять публикацию продукта')
can_change_product_description, created = Permission.objects.get_or_create(codename='can_change_product_description', name='Может менять описание продукта')
can_change_product_category, created = Permission.objects.get_or_create(codename='can_change_product_category', name='Может менять категорию продукта')

# Добавляем разрешения для модераторов
moderator_group.permissions.add(
    can_cancel_product_publication,
    can_change_product_description,
    can_change_product_category
)
