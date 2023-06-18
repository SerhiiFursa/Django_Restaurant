from django import forms

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = (
            'client_name',
            'client_email',
            'client_phone',
            'table_number',
            'number_of_guests',
            'reservation_time',
            'reservation_time_end',
            'reservation_date'
        )
