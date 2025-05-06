from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('download/excel/', views.download_excel, name='download_excel'),
        path('download/csv/', views.download_csv, name='download_csv'),
        path('download/pdf/', views.download_pdf, name='download_pdf'),
]
