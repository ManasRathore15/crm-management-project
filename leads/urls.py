from django.urls import path

from .views import home, login_view, dashboard_view, logout_view



urlpatterns = [

    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),



]