
from django.contrib.auth.models import User
from .models import ResetPasswordToken
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.views import APIView
from rest_framework.response import Response
from rest_framework import  status

import random, string


# Create your views here.

class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        email = request.data['email']
        user = User.objects.get(email=email)
        current_site = get_current_site(request)
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _i in range(12))

        ResetPasswordToken.objects.create(
            email=email,token=token,
        )

        message = render_to_string("/password_reset_email.html", {
            'user':user,
            'token':token,
        })

        send_mail(
            subject='Password Reset Link',
            message=message,
            recipient_list=[email],
            from_email= 'nehatkhan82@gmail.com',
        )
        return Response({'message':'Reset Link Send Successfully'}, status=status.HTTP_200_OK)



    