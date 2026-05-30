from django.urls import path

from .views import home, login_view, dashboard_view, logout_view, update_status, export_csv, assign_agent, agents_view, overview_view



urlpatterns = [

    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('update-status/<int:lead_id>/', update_status, name='update_status'),
    path('export-csv/',export_csv, name='export_csv'),
    path('assign-agent/<int:lead_id>/', assign_agent, name='assign_agent'),
    path('agents/', agents_view, name='agents'),
    path('overview/', overview_view, name='overview'),

]