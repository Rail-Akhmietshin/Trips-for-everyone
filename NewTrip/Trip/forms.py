import re
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from datetime import datetime
from .utils import cities


class AddTripForm(forms.ModelForm):
    ''' A form for publish trip. '''
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddTripForm, self).__init__(*args, **kwargs)
        self._user = user


    class Meta:
        model = Trip

        fields = ['where_from', 'where', 'date_trip', 'time_trip', 'cost', 'two_people', 'empty_baggage',
                  'without_animals', 'additional_inf']
        widgets = {
            'where_from' : forms.TextInput(attrs={'placeholder': "Откуда выезжаете?", 'maxlength' : 30}),
            'where' : forms.TextInput(attrs={'placeholder' : 'Куда едете?', 'maxlength' : 30}),
            'date_trip' : forms.TextInput(attrs={'type' : 'date', 'min' : f'{datetime.now().strftime("%Y-%m-%d")}', 'max' : '2024-01-01'}),
            'time_trip' : forms.DateInput(attrs={'type' : 'time'}),
            'cost' : forms.TextInput(attrs={'placeholder': "Цена за одного человека", 'min' : 50, "max" : 10000}),
            'additional_inf': forms.Textarea(attrs={'placeholder': "Доп. сведения", 'maxlength' : 100}),
        }

    def clean_where_from(self):
        where_from = self.cleaned_data["where_from"]

        if where_from.title() not in cities:
            raise ValidationError("Такого города в России не существует")

        return where_from.title()

    def clean_where(self):

        where = self.cleaned_data["where"]

        if where.title() not in cities:
            raise ValidationError("Такого города в России не существует")


        return where.title()

    def clean_time_trip(self):

        time_trip = self.cleaned_data["time_trip"]

        test_time_trip = time_trip.partition(':')

        if datetime.now().strftime("%Y-%m-%d") == self.cleaned_data["date_trip"] and\
                (int(test_time_trip[0])+1 <= datetime.now().hour and
                 (int(test_time_trip[2]) <= datetime.now().minute or int(test_time_trip[2]) >= datetime.now().minute)):

            raise ValidationError("Невозможно установить такое время поездки")

        return time_trip

    def clean_cost(self):

        cost = self.cleaned_data["cost"]

        if cost > 10000:
            raise ValidationError("Цена не может быть выше 10000р.")

        if cost < 50:
            raise ValidationError("Цена не может быть ниже 50р.")

        return cost

    def clean_additional_inf(self):

        additional_inf = self.cleaned_data["additional_inf"]

        if re.findall("[^а-яА-ЯёЁ\,\.\s]+", additional_inf):
            raise ValidationError("Должны присутствовать исключительно латинские символы, '-', '.' и пробелы")

        return additional_inf

    def clean(self):
        cleaned_data = super().clean()

        where_from = cleaned_data.get("where_from")
        where = cleaned_data.get("where")

        date_trip = cleaned_data.get("date_trip")

        if Trip.objects.filter(where_from=where_from, where=where, date_trip=date_trip, trip_user=self._user).exists():
            raise ValidationError('Разрешено не более 1 поездки в день по заданному маршруту')


        if where_from and where:
            if where.title() == where_from.title() or where_from.title() == where.title():
                raise ValidationError("Одинаковые города недопустимы")



class AuthUserForm(AuthenticationForm):
    """ A form for authorization users. """
    username = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Номер телефона"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))


class UserCreationForm(forms.ModelForm):
    """ A form for registration users. """
    number_phone = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Номер телефона"}))
    username = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={"placeholder": "Ваше имя"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}))


    class Meta:
        model = MyUser
        fields = ("number_phone", "username", 'password1', 'password2')
        widgets = {
            "number_phone": forms.NumberInput(attrs={"placeholder": "Номер телефона"}),
            "username": forms.TextInput(attrs={"placeholder": "Ваше имя"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Пароль"}),
            "password2": forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def clean_username(self):
        username = self.cleaned_data["username"]

        if re.findall("[^а-яА-ЯёЁ\s]+", username):
            raise ValidationError("Должны присутствовать исключительно латинские символы и пробелы")

        return username.title()

    def clean_number_phone(self):
        number_phone = self.cleaned_data["number_phone"]

        if not re.findall("89[0-9]{9}", str(number_phone)):
            raise ValidationError("Номер должен состоять из 11 цифр и начинаться с 89")

        return number_phone




    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('number_phone', 'password', 'username', 'is_active', 'is_admin')
