# Generated by Django 5.0.3 on 2024-03-16 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('set_published', 'Может отменять публикацию'), ('change_description', 'Может изменять описание продукта'), ('change_category', 'Может изменять гатегорию')], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]