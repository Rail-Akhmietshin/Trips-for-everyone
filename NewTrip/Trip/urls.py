from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path("", FindTripMain.as_view(), name='main'),
    path("trips/", cache_page(180)(Trips.as_view()), name='trips'),
    path('new_trip/', AddTrip.as_view(), name='new_trip'),
    path('auth/', AuthUser.as_view(), name='auth'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>', ShowPost.as_view(), name='post')


    # re_path(r"^trips/(?P<where_from>[0-9]{4})/", re_archive),      # задание url с помощью регулярных выражений

]



# str – любая не пустая строка, исключая символ ‘/’
#   int – любое положительное целое число, включая 0
# slug – слаг, то есть, латиница ASCII таблицы, символы дефиса и подчеркивания
#   uuid – цифры, малые латинские символы ASCII, дефис
# path – любая не пустая строка, включая символ ‘/’