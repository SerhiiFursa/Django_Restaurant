from django.utils.crypto import salted_hmac
import six


class ReservationTokenGenerator:
    def make_token(self, reservation):
        # Generate a token using the reservation attributes
        value = str(reservation.pk) + str(reservation.confirmed) + reservation.client_email
        return salted_hmac(six.text_type(value), 'my_secret_key').hexdigest()

    def check_token(self, reservation, token):
        # Check if the token is valid for the given reservation
        expected_token = self.make_token(reservation)
        return token == expected_token


reservation_token_generator = ReservationTokenGenerator()
