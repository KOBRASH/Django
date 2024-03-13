import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify as django_slugify

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, unique=True, verbose_name='Slug')
    content = models.TextField(null=True, blank=True, verbose_name='Содержание')
    preview = models.ImageField(upload_to='blog_previews/', null=True, blank=True, verbose_name='Превью')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    published = models.BooleanField(default=False, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'

    def save(self, *args, **kwargs):
        if not self.slug:
            random_slug = str(uuid.uuid4())[:8]
            self.slug = django_slugify(random_slug, allow_unicode=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.slug])
