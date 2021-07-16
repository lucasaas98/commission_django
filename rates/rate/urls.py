from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('calculatetotal',  views.calculate_total, name='calculatetotal'),
    path('calculatemonthly',  views.calculate_monthly, name='calculatemonthly'),
    path('calculatecity',  views.calculate_city, name='calculatecity'),
]