from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('write/', views.write, name='write'),
    path('people/', views.people_view, name='people'),
    path('day/', views.day, name='day'),
    path('delete_day/', views.delete_day, name='delete_day'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)