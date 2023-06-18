"""
In this file, the working_hours function generates a list of time slots corresponding
to the restaurant time. The function also takes into account the day.
For example, if the reservation is for today and the current time is 12:00,
slots from 14:00 will be added to the list. If another day is selected,
all slots will be added according to the restaurant's opening hours.

The working_days function generates a list of dates for the reservation.
If today's date is selected and the restaurant is no longer open,
then this date will not be added
"""


def working_hours(reservation_date=None):
    import datetime

    today = datetime.date.today()
    if reservation_date != str(today):
        time_list = []
        for hour in range(10, 21):
            time_obj = datetime.time(hour=hour, minute=0)
            time_list.append(time_obj)
        return time_list

    else:
        now = datetime.datetime.now()
        start_hour = now.hour + 2
        time_list = []
        for hour in range(start_hour, 21):
            time_obj = datetime.time(hour=hour, minute=0)
            time_list.append(time_obj)
        if len(time_list) == 0:
            time_list.append('Unfortunately, all tables are occupied.')
        return time_list


def working_days():
    from datetime import datetime, timedelta

    current_date = datetime.now().date()
    now = datetime.now()
    if now.hour >= 20:
        current_date += timedelta(days=1)
    dates_list = []

    # Generate dates two weeks ahead
    for _ in range(14):
        dates_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    return dates_list
