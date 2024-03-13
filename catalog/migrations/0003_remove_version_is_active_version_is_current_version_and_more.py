# Generated by Django 5.0.3 on 2024-03-12 22:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_version'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='is_active',
        ),
        migrations.AddField(
            model_name='version',
            name='is_current_version',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='version',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product'),
        ),
        migrations.AlterField(
            model_name='version',
            name='version_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='version',
            name='version_number',
            field=models.CharField(max_length=50),
        ),
    ]