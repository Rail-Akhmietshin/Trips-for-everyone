from django.contrib.auth import logout, login

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q

from django.http import HttpResponseNotFound, Http404, HttpResponseForbidden, HttpResponseServerError

from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DetailView


from .forms import *
from .models import *
from .utils import DataMixin




class FindTripMain(DataMixin, ListView):
    model = Trip
    template_name = 'Trip/main.html'

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='NewWay - Поиск попутчиков!')

        return dict(list(context.items()) + list(c_def.items()))





class Trips(DataMixin, ListView):
    model = Trip

    template_name = 'Trip/find.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='Текущие поездки')

        return dict(list(context.items()) + list(c_def.items()))


    def get_queryset(self):
        query_where_from = self.request.GET.get('where_from')
        query_where = self.request.GET.get('where')

        if query_where_from.title() not in cities or query_where.title() == query_where_from.title():
            raise Http404()

        query_when = self.request.GET.get('when')


        posts = Trip.objects.filter(
            Q(where_from__icontains=query_where_from) & Q(where__icontains=query_where) &  Q(date_trip__icontains=query_when)
        )


        return posts


class ShowPost(DataMixin, DetailView):
    template_name = 'Trip/post.html'
    model = Trip
    slug_url_kwarg = "post_slug"
    context_object_name = "post"


    def get_context_data(self, *, object_list = None, **kwargs):

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Текущая поездка')
        return dict(list(context.items()) + list(c_def.items()))



class AddTrip(LoginRequiredMixin, DataMixin, CreateView):
    model = Trip
    form_class = AddTripForm
    template_name = "Trip/publish.html"
    #success_url = reverse_lazy("main")
    login_url = reverse_lazy("auth")
    # raise_exception = True  # вызов ошибки 403

    def form_valid(self, form):

        form.instance.trip_user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)


        c_def = self.get_user_context(title='Публикация поездки')


        return dict(list(context.items()) + list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super(AddTrip, self).get_form_kwargs()
        kwargs.update({'user': self.request.user.pk})
        return kwargs


    def get_success_url(self):
        form_where_from = self.request.POST.get('where_from')
        form_where = self.request.POST.get('where')
        form_when = self.request.POST.get('date_trip')

        url = f'?where_from={form_where_from}&where={form_where}&when={form_when}'
        slug = slugify(f'{url}&{self.request.user.pk}{self.request.user.number_phone}{self.request.user.pk}').lower()

        return str(f'/post/{slug}')










class AuthUser(DataMixin, LoginView):
    form_class = AuthUserForm
    template_name = "Trip/input.html"
    # success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='Авторизация')

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('main')


class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'Trip/reg.html'
    success_url = reverse_lazy('auth')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title='Регистрация')

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


def logout_user(request):
    logout(request)
    return redirect('main')


def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1> Такой страницы не существует </h1> <a>{redirect('main')}</a>")

def AccessIsDenied(request, exception):
    return HttpResponseForbidden(f"<h1> Доступ запрещен </h1> <a>{redirect('main')}</a>")

def ServerError(exception):
    return HttpResponseServerError(f"<h1> Ошибка сервера </h1> <a>{redirect('main')}</a>")


