from django.conf import settings
import pyotp
from accounts.models import UserProfile
from twilio.rest import Client


def admin_login(request):
    totp = pyotp.TOTP(UserProfile.totp_secret)
    code = totp.now()  # this generates the current 6-digit code
    client = Client(settings.OTP_TWILIO_ACCOUNT, settings.OTP_TWILIO_AUTH)
    message = client.messages.create(
        body=f"Your Django admin login code is: {code}",
        from_=settings.OTP_TWILIO_FROM,
        to=UserProfile.phone_number  # e.g. "+14379845385"
    )
    request.session['pre_2fa_user_id'] = user.id
