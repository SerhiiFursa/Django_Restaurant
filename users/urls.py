from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.main, name='main'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_details/', views.contact_details, name='contact_details'),
    path('reservation_data/', views.reservation_data, name='reservation_data'),
    path('get_time_slots/', views.get_time_slots, name='get_time_slots'),
    path('send_confirmation_email/', views.send_confirmation_email, name='send_confirmation_email'),
    path('reservation_check_email/', views.reservation_check_email, name='reservation_check_email'),
    path('reservation_confirmed/<str:uidb64>/<str:token>/', views.reservation_confirmed, name='reservation_confirmed'),
    path('confirm_reservation/<str:uidb64>/<str:token>/', views.confirm_reservation, name='confirm_reservation'),
    path('check_reservation/', views.check_reservation, name='check_reservation'),
    path('reservation_delete/', views.reservation_delete, name='reservation_delete')

]
