from django.urls import path
from . import views

app_name = 'admin_app'

urlpatterns = [
    path('admin_reservations/', views.admin_reservations, name='admin_reservations'),
    path('admin_reservation_detail/<int:reservation_id>/', views.admin_reservation_detail, name='admin_reservation_detail'),
    path('admin_confirm_visit/<int:reservation_id>/', views.admin_confirm_visit, name='admin_confirm_visit'),
]

