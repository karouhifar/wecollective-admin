import time
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
import pyotp
from accounts.models import UserProfile
from twilio.rest import Client


def admin_login(request):
    # If already passed 2FA, redirect to admin index
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/admin/')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active and user.is_staff and user.is_superuser:

            totp = pyotp.TOTP(user.profile.totp_secret)
            code = totp.now()  # this generates the current 6-digit code
            # Send SMS via Twilio
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID,
                                settings.TWILIO_AUTH_TOKEN)
                print("mesgage pending", settings.TWILIO_ACCOUNT_SID)
                print("mesgage pending", settings.OTP_TWILIO_FROM)
                msg = client.messages.create(
                    body=f"Your Mundus admin login code is: {code}. Please don't share this code with anyone.",
                    from_=settings.OTP_TWILIO_FROM,
                    to=user.profile.phone_number  # e.g. "+14379845385"
                )
                print("mesgage sent", msg)
            except Exception as e:
                print("Error sending SMS:", e)
                error = 'Failed to send OTP. Please try again later.'
                return render(request, 'admin_login.html', {'error': error})

            # Store partial-auth state in session
            request.session['pre_2fa_user_id'] = user.id
            request.session['pre_2fa_timestamp'] = int(time.time())
            # Optionally store next URL
            next_url = request.GET.get('next')
            if next_url:
                request.session['pre_2fa_next'] = next_url

            return redirect('admin_otp_verify')
        else:
            error = 'Invalid credentials or not authorized.'
    return render(request, 'admin_login.html', {'error': error})

###################################################################


def admin_otp_verify(request):
    error = None
    # Ensure the user passed the first step
    user_id = request.session.get('pre_2fa_user_id')
    print("HI", user_id)
    if not user_id:
        return redirect('admin_login')  # no partial-auth state
    # Optional: enforce a timeout (e.g. 5 minutes)
    timestamp = request.session.get('pre_2fa_timestamp', 0)
    print("HI 2", timestamp)
    if time.time() - timestamp > 300:  # 300 seconds = 5 minutes
        request.session.flush()
        error = 'Session expired—please log in again.'
        return render(request, 'admin_login.html', {'error': error})
    if request.method == 'POST':
        code = request.POST.get('otp_code', '').strip()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('admin_login')

        # Verify the OTP code
        print("User profile", user.profile.totp_secret)
        totp = pyotp.TOTP(user.profile.totp_secret)
        if totp.verify(code, valid_window=1):
            # OTP valid: perform full login
            login(request, user)
            # Clear pre-2FA session keys
            next_url = request.session.pop('pre_2fa_next', None)
            request.session.pop('pre_2fa_user_id', None)
            request.session.pop('pre_2fa_timestamp', None)
            return redirect(next_url or '/admin/')
        else:
            error = 'Invalid code, please try again.'
     # Render OTP form on GET or after failure
    return render(request, 'admin_otp_verify.html', {'error': error})
