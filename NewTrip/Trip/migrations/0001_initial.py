# Generated by Django 4.0.5 on 2022-07-09 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('number_phone', models.PositiveBigIntegerField(blank=True, db_index=True, unique=True, verbose_name='номер телефона')),
                ('username', models.CharField(db_index=True, max_length=20, verbose_name='Имя пользователя')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'пользователя',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['number_phone', 'username'],
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('where_from', models.CharField(max_length=30, verbose_name='Откуда')),
                ('where', models.CharField(max_length=30, verbose_name='Куда')),
                ('date_trip', models.CharField(max_length=10, verbose_name='Когда')),
                ('time_trip', models.CharField(max_length=5, verbose_name='Во сколько')),
                ('cost', models.PositiveSmallIntegerField(verbose_name='Цена')),
                ('additional_inf', models.TextField(blank=True, verbose_name='Доп. информация')),
                ('two_people', models.BooleanField(default=False, verbose_name='Двое сзади')),
                ('empty_baggage', models.BooleanField(default=False, verbose_name='Пустой багажник')),
                ('without_animals', models.BooleanField(default=False, verbose_name='Без животных')),
                ('slug_trips', models.SlugField(max_length=255, verbose_name='URL_trips')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Trip_URL')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('trip_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователи')),
            ],
            options={
                'verbose_name': 'поездку',
                'verbose_name_plural': 'Существующие поездки',
                'ordering': ['time_trip', '-cost'],
            },
        ),
    ]
