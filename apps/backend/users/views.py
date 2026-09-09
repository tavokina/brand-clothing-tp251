from rest_framework import generics, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from users.serializers import RegisterSerializer
from users.tokens import account_activation_token
from users.utils import send_activation_email

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        send_activation_email(self.request, user)



class ActivateAccountView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save(update_fields=["is_active"])
            return Response(template_name="users/activation_success.html")

        return Response(template_name="users/activation_invalid.html", status=400)


class ResendActivationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email, is_active=False)
        except User.DoesNotExist:
            return Response({"detail": "If the account exists, email was sent."})
        send_activation_email(request, user)
        return Response({"detail": "If the account exists, email was sent."})
