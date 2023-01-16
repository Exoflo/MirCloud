from django.urls import path
from . import views

#urlconfs
urlpatterns = [
    path('', views.Login_view, name = "Login"),
    path('login/', views.Login_view, name ="Login"),
    path('index/', views.SearchForm_view, name = "SearchForm")
]