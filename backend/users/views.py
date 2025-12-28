import logging
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import EmailOTP
from .utils import generate_otp

logger = logging.getLogger(__name__)


# ------------------ SIGNUP ------------------
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = str(request.data.get("email", "")).strip().lower()
        password = str(request.data.get("password", "")).strip()
        role = str(request.data.get("role", "")).strip()

        if not email or not password or not role:
            return Response({"detail": "email, password and role are required"}, status=400)

        if User.objects.filter(username=email).exists():
            return Response({"detail": "User already exists"}, status=400)

        user = User.objects.create_user(username=email, email=email, password=password)
        user.profile.role = role
        user.profile.email_verified = False
        user.profile.save()

        otp = str(generate_otp())

        EmailOTP.objects.filter(email=email).delete()

        EmailOTP.objects.create(
            email=email,
            otp=otp,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        logger.warning(f"OTP for {email} is {otp}")

        return Response({"detail": "OTP sent"}, status=201)


# ------------------ VERIFY OTP ------------------
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        raw_email = request.data.get("email")
        raw_otp = request.data.get("otp")

        email = str(raw_email).strip().lower()
        otp = str(raw_otp).strip()

        logger.warning(f"VERIFY email='{email}' otp='{otp}'")

        if not email or not otp:
            return Response({"detail": "email and otp are required"}, status=400)

        record = EmailOTP.objects.filter(email=email).order_by("-id").first()

        if not record:
            return Response({"detail": "Invalid email"}, status=400)

        if record.expires_at < timezone.now():
            record.delete()
            return Response({"detail": "OTP expired"}, status=400)

        # 🔥 Force string-safe compare
        if str(record.otp).strip() != otp:
            logger.warning(f"OTP MISMATCH: DB='{record.otp}' USER='{otp}'")
            return Response({"detail": "Invalid OTP"}, status=400)

        user = User.objects.get(username=email)
        user.profile.email_verified = True
        user.profile.save()

        record.delete()

        return Response({"detail": "Email verified successfully"}, status=200)


# ------------------ LOGIN ------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = str(request.data.get("email", "")).strip().lower()
        password = str(request.data.get("password", "")).strip()

        if not email or not password:
            return Response({"detail": "email and password required"}, status=400)

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=400)

        if not user.check_password(password):
            return Response({"detail": "Wrong password"}, status=400)

        if not user.profile.email_verified:
            return Response({"detail": "Email not verified"}, status=403)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=200)
