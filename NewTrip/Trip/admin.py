from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import *





class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('number_phone', 'username', 'last_login', 'is_admin', 'is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('number_phone', 'password')}),
        ('Personal info', {'fields': ('username', 'last_login')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('number_phone', 'username', 'password1', 'password2'),
        }),
    )

    search_fields = ('number_phone', 'username')
    ordering = ('id',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)


class TripAdmin(admin.ModelAdmin):
    list_display = ('where_from', 'where', 'date_trip', 'time_trip', 'cost', 'additional_inf',
                    'time_create')
    list_display_links = ('where_from', 'where', 'date_trip', 'time_trip', 'time_create')
    search_fields = ('where_from', 'where', 'date_trip', 'time_trip')
    list_filter = ('date_trip', 'time_create')

    prepopulated_fields = {"slug_trips" : ("where_from", "where", "date_trip")}


admin.site.register(Trip, TripAdmin)
