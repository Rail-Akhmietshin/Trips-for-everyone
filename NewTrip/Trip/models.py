from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.urls import reverse
# from django.utils.text import slugify
from slugify import slugify

class MyUserManager(BaseUserManager):


    def create_user(self, number_phone, username, password=None):

        if not number_phone:
            raise ValueError("Номер телефона обязателен")

        user = self.model(
            number_phone = number_phone,
            username = username,
        )


        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, number_phone, username, password=None):

        user = self.create_user(
            number_phone, password = password, username = username
        )

        user.is_admin = True
        user.save(using=self._db)

        return user



class MyUser(AbstractBaseUser):
    """ The table for registered users. """
    number_phone = models.PositiveBigIntegerField(db_index=True, unique=True, blank=True, verbose_name='номер телефона')
    username = models.CharField(max_length=20, db_index=True, verbose_name='Имя пользователя')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()



    USERNAME_FIELD = 'number_phone'     # Уникальные идентификаторы пользователей.
    REQUIRED_FIELDS = ['username']      # Список имен полей, которые будут запрашиваться при создании суперпользователя.

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'
        ordering = ['is_admin', 'number_phone', 'username']

    def __str__(self):
        return self.number_phone



    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Trip(models.Model):
    """ The table for trips. """
    where_from = models.CharField(max_length=30, verbose_name='Откуда')
    where = models.CharField(max_length=30, verbose_name='Куда')
    date_trip = models.CharField(max_length=10, verbose_name='Когда')
    time_trip = models.CharField(max_length=5, verbose_name='Во сколько')
    cost = models.PositiveSmallIntegerField(verbose_name='Цена')
    additional_inf = models.TextField(blank=True, verbose_name='Доп. информация')
    two_people = models.BooleanField(default=False, verbose_name='Двое сзади')
    empty_baggage = models.BooleanField(default=False, verbose_name='Пустой багажник')
    without_animals = models.BooleanField(default=False, verbose_name='Без животных')

    slug_trips = models.SlugField(max_length=255, db_index=True, verbose_name='URL_trips')

    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='Trip_URL')


    trip_user = models.ForeignKey('MyUser', on_delete=models.PROTECT, verbose_name='Пользователи', null=True)


    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')



    def save(self, *args, **kwargs):
        self.slug_trips = f'?where_from={self.where_from}&where={self.where}&when={self.date_trip}'
        self.slug = slugify(f'{self.slug_trips}&{self.trip_user.pk}{self.trip_user.number_phone}{self.trip_user.pk}').lower()
        super(Trip, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug_trips


    def get_absolute_url(self):
        return reverse('post', kwargs = {'post_slug' : self.slug})

    class Meta:
        verbose_name = 'поездку'
        verbose_name_plural = 'Существующие поездки'
        ordering = ['time_trip', '-cost']





