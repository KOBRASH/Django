from django import template
from django.conf import settings
from urllib.parse import urljoin

register = template.Library()


@register.simple_tag
def mediapath(image_path):
    # Получаем базовый URL для медиафайлов из настроек Django
    media_url = getattr(settings, 'MEDIA_URL', '/media/')

    # Объединяем базовый URL медиафайлов и переданный путь к изображению
    full_media_url = urljoin(media_url, image_path)

    return full_media_url
