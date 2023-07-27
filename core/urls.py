from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path('create/certificate/', views.create_certificate, name="create_new_certificate"),
    path('view/certificate/<int:id>/', views.view_certificate, name="view_certificate_file"),
    path('file/<int:id>/', views.gen_cert_pdf, name="file_download"),
    path('generate_token/<int:id>/', views.generate_token, name="generate_token"),
    path('verify_token/', views.verify_token, name='verify_token'),
    path('update_certificate/<int:id>/', views.update_certificate, name="update_certificate"),

]
