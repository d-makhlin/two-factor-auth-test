import smtplib
from typing import Optional
from email.message import EmailMessage
from users.models import User
from django.utils.encoding import force_bytes

from django.utils.http import urlsafe_base64_encode
from users.services.tokens_service import account_activation_token


class UserService:
    def init_account_verification(user: User, email: str) -> str:
        token = account_activation_token.make_token(user)
        content = f"http://localhost:8000/api/users/auth/verify/?id={urlsafe_base64_encode(force_bytes(user.pk))}&token={token}"
        UserService._send_otp_message(content, email)
        return content

    def check_account_token(user: Optional[User], token: str) -> bool:
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return True
        return False

    def _send_otp_message(content: str, send_to: str) -> None:
        sender = "twostepauth@noreply.com"

        message = f"""\
            Subject: test notification mail
            To: {send_to}
            From: {sender}
            Use this link to confirm your account."""

        #   Connect here to a real smtp server

        # with smtplib.SMTP("localhost", 1025) as server:
        # server.sendmail(sender, send_to, message)
