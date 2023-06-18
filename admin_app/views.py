
from django.shortcuts import render, redirect, get_object_or_404

from admin_app.logic.reservation_table import reservation_table
from users.models import Reservation


def admin_reservations(request):
    """
    The function creates a table where columns are time slots and rows are table numbers.
    The cells in the table show whether there is a corresponding reservation or not.
    The table is created for the selected date
    """

    if not request.user.is_authenticated:
        return redirect('admin:index')
    else:
        selected_date = request.GET.get('date')
        if selected_date:
            reservations = Reservation.objects.filter(reservation_date=selected_date).order_by('table_number',
                                                                                               'reservation_time')
        else:
            reservations = Reservation.objects.none()

        reservation_list, time_slots = reservation_table(reservations)

        context = {
            'reservation_list': reservation_list,
            'time_slots': time_slots,
            'selected_date': selected_date,
        }

        return render(request, 'admin_reservations.html', context)


def admin_reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    context = {'reservation': reservation}
    return render(request, 'admin_reservation_detail.html', context)


def admin_confirm_visit(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.confirmed_visit = True
    reservation.save()
    return redirect('admin_app:admin_reservations')
