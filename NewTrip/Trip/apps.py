from django.apps import AppConfig


class TripConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Trip'
    verbose_name = 'Все поездки'        # название категории таблицы поездок в админке
