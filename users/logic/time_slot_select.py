"""
    The function selects free time slots considering the selected date and the selected table.
    The slots correspond to the restaurant's work schedule (from 10:00 to 22:00).
    A table is reserved for 2 hours, so if the database has a reservation for,
    for example, 15:00, then the slot at 14:00 will not be available.
"""

from django.db.models import Max
import datetime

from users.logic.time_and_date import working_hours
from users.models import Reservation


def time_slot_select(table_id, reservation_date):

    existing_reservations = Reservation.objects.filter(table_number=table_id,
                                                       reservation_date=reservation_date,
                                                       confirmed=1)

    max_end_time = existing_reservations.aggregate(Max('reservation_time_end'))['reservation_time_end__max']

    all_time_slots = [datetime.datetime.strptime(str(time), '%H:%M:%S').strftime('%H:%M') for time in
                      working_hours(reservation_date)]

    reservation_date = datetime.datetime.strptime(reservation_date, '%Y-%m-%d').date()

    available_time_slots = []

    existing_reservation_times = [reservation.reservation_time for reservation in existing_reservations]

    min_start_time = min(existing_reservation_times) if existing_reservation_times else None

    for time_slot in all_time_slots:
        time_slot_start = datetime.datetime.combine(reservation_date,
                                                    datetime.datetime.strptime(time_slot, '%H:%M').time())
        time_slot_end = time_slot_start + datetime.timedelta(hours=1)

        if max_end_time is None or (max_end_time < time_slot_start.time() or min_start_time > time_slot_end.time()):
            is_available = True

            for reservation in existing_reservations:
                reservation_start = datetime.datetime.combine(reservation.reservation_date,
                                                              reservation.reservation_time)
                reservation_end = datetime.datetime.combine(reservation.reservation_date,
                                                            reservation.reservation_time_end)

                if reservation_start <= time_slot_start and time_slot_end <= reservation_end:
                    is_available = False

            if is_available:
                available_time_slots.append(time_slot)

    return available_time_slots, max_end_time
