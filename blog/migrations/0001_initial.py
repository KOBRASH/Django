# Generated by Django 5.0.3 on 2024-03-12 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('content', models.TextField()),
                ('preview_image', models.ImageField(blank=True, null=True, upload_to='blog_previews/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_published', models.BooleanField(default=False)),
                ('views', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
