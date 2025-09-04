import os
from celery import Celery

# Указываем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prodcast_worker.settings')

# Создаём объект Celery
app = Celery('prodcast_worker')

# Подключаем настройки из Django (будет искать CELERY_*)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически подхватывать tasks.py из приложений
app.autodiscover_tasks()
