from datetime import date, datetime, timedelta
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from users.models import Reservation


@shared_task
def delete_non_compliant_reservations():  # this function deletes unconfirmed or outdated reservations
    current_date = date.today()

    # Define the time range for collecting reservation_id (from 10:00 to 22:00)
    start_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=9)
    end_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=22)

    reservation_ids = Reservation.objects.filter(reservation_date=current_date,
                                                 reservation_time__range=(start_time.time(),
                                                                          end_time.time())).values_list('id', flat=True)

    for reservation_id in reservation_ids:
        try:
            reservation = Reservation.objects.get(id=reservation_id)

            if not reservation.is_confirmed:
                # Calculating the time difference between the current time and the reservation time
                time_difference = timezone.now() - datetime.combine(current_date, reservation.reservation_time)

                # If more than 20 minutes have passed since the reservation, and it is not confirmed, delete it
                if time_difference.total_seconds() > 1200:
                    reservation.delete()

            if reservation.is_confirmed:
                end_time = datetime.combine(current_date, reservation.reservation_time) + timedelta(hours=2)
                time_difference = timezone.now() - end_time

                # If more than 2 hours have passed since the end of the reservation, delete it
                if time_difference.total_seconds() > 7200:
                    reservation.delete()

        except ObjectDoesNotExist:
            pass
