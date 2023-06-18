
def reservation_table(reservations=None):

    time_slots = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00']

    reservation_list = []
    for table_number in range(1, 28):
        table_row = []
        for time_slot in time_slots:
            reservation = reservations.filter(table_number=table_number,
                                              reservation_time=time_slot).first()
            table_row.append(reservation)
        reservation_list.append((table_number, table_row))

    return reservation_list, time_slots
