from django.urls import path

from .views import home, login_view, dashboard_view, logout_view, update_status, export_csv



urlpatterns = [

    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('update-status/<int:lead_id>/', update_status, name='update_status'),
    path('export-csv/',export_csv, name='export_csv'),

]