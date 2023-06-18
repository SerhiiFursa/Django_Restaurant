from django.db import models
from django.utils.crypto import get_random_string


class Reservation(models.Model):
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField(unique=True)
    client_phone = models.CharField(max_length=20)
    table_number = models.IntegerField(default=None)
    number_of_guests = models.IntegerField()
    reservation_time = models.TimeField()
    reservation_time_end = models.TimeField()
    reservation_date = models.DateField()
    confirmed = models.BooleanField(default=False)
    confirmed_visit = models.BooleanField(default=False)
    uidb64 = models.CharField(max_length=64, blank=True)
    token = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        if not self.uidb64:
            self.uidb64 = get_random_string(64)
        if not self.token:
            self.token = get_random_string(64)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.client_name


class Table(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()
