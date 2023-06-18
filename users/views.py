from datetime import datetime, timedelta

import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .forms import ReservationForm
from .logic.time_slot_select import time_slot_select
from .logic.time_and_date import  working_days
from .models import Reservation, Table
from .token import reservation_token_generator


def main(request):
    return render(request, 'main.html')


def contact_details(request):
    reservation_date = working_days()
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        client_phone = request.POST.get('client_phone')
        number_of_guests = request.POST.get('number_of_guests')
        reservation_date = request.POST.get('reservation_date')

        request.session['client_name'] = client_name
        request.session['client_email'] = client_email
        request.session['client_phone'] = client_phone
        request.session['number_of_guests'] = number_of_guests
        request.session['reservation_date'] = reservation_date
        return redirect('users:reservation_data')
    return render(request, 'contact_details.html', {'reservation_date': reservation_date})


def reservation_data(request):
    client_email = request.session.get('client_email')
    email = Reservation.objects.filter(client_email=client_email)

    # The choice of tables according to their capacity, depending on the number of guests
    guests = request.session.get('number_of_guests')
    tables = Table.objects.filter(capacity__gte=guests, capacity__lte=str(int(guests) + 2))

    tables = [table.number for table in tables]
    if request.method == 'POST':
        client_name = request.session.get('client_name')
        client_email = request.session.get('client_email')
        client_phone = request.session.get('client_phone')
        number_of_guests = request.session.get('number_of_guests')
        reservation_date = request.session.get('reservation_date')

        table_number = request.POST.get('table_number')
        reservation_time = request.POST.get('reservation_time')
        reservation_time_end = (datetime.strptime(reservation_time, '%H:%M') + timedelta(hours=1)).time()
        data = {
            'client_name': client_name,
            'client_email': client_email,
            'client_phone': client_phone,
            'number_of_guests': number_of_guests,
            'reservation_date': reservation_date,
            'table_number': table_number,
            'reservation_time': reservation_time,
            'reservation_time_end': reservation_time_end
        }

        form = ReservationForm(data)
        if form.is_valid():
            reservation = Reservation.objects.create(**data)
            request.session['reservation_id'] = reservation.pk
            return redirect('users:send_confirmation_email')

    return render(request, 'reservation_data.html', {'tables': tables, 'email': email})


def get_time_slots(request):
    # generating and passing time slots to the time_slots.js script so that when the user
    # selects a table number, the corresponding time slots are displayed without reloading the page

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        table_id = data.get('table_id')

        reservation_date = request.session.get('reservation_date')

        available_time_slots, max_end_time = time_slot_select(table_id, reservation_date)

        return JsonResponse({'time_slots': available_time_slots,
                             'max_end_time': max_end_time.strftime('%H:%M') if max_end_time else None})

    return JsonResponse({'error': 'Invalid request'}, safe=False)


def send_confirmation_email(request):
    reservation_id = request.session.get('reservation_id')
    reservation = Reservation.objects.get(pk=reservation_id)
    subject = 'Booking confirmation'
    from_email = settings.EMAIL_HOST_USER
    to_email = reservation.client_email

    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(reservation.id))
    token = reservation_token_generator.make_token(reservation)

    email_message = render_to_string('reservation_confirmation_email.html', {
        'reservation': reservation,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
    })
    send_mail(subject, email_message, from_email, [to_email], html_message=email_message)

    return redirect('users:reservation_check_email')


def confirm_reservation(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    reservation = get_object_or_404(Reservation, id=uid)
    if not reservation.confirmed and reservation_token_generator.check_token(reservation, token):
        reservation.confirmed = True
        reservation.save()
        return redirect('users:reservation_confirmed', uidb64=uidb64, token=token)

    return render(request, 'reservation_not_found.html')


def reservation_check_email(request):
    return render(request, 'reservation_check_email.html')


def reservation_confirmed(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    reservation = get_object_or_404(Reservation, id=uid)

    return render(request, 'reservation_confirmed.html', {'reservation': reservation})


def check_reservation(request):
    if request.method == 'POST':
        email = request.POST.get('client_email')
        reservation = Reservation.objects.filter(client_email=email)

        if reservation:
            return render(request, 'check_reservation.html', {'reservation': reservation})
        else:
            return render(request, 'reservation_not_found.html')


def reservation_delete(request):
    email = request.GET.get('client_email')
    Reservation.objects.filter(client_email=email).delete()
    return render(request, 'reservation_delete.html', {'email': email})


def about_us(request):
    return render(request, 'about_us.html')
