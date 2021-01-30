# import from django framework
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

# import from django rest frameworkensure
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_201_CREATED,
    HTTP_200_OK)

# import from this apps
from .serializers import *
from .utils import maketicket, checkticket, maketoken
from .models import Ticket, Token

# import from python
import datetime
import json
from uuid import uuid4
User = get_user_model()


@api_view(['POST'])
def signin(request):
    serializer = SigninSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        user = User.objects.filter(email=data['email']).first()
        response = model_to_dict(user, exclude=["password"])
        response['access'] = str(maketoken(user))
        response['thumbnail'] = response['thumbnail'].url
        return Response(response, HTTP_200_OK)
    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():

        data = serializer.validated_data
        instance = User.objects.create(
            email=data.get('email'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            password=make_password(data.get('password')),
        )
        newuser = model_to_dict(instance, exclude=["password"])

        maildata = {"ticket": maketicket(instance)}
        maildata.update(newuser)

        html = render_to_string('email/verify_email.html', maildata)
        send_mail(
            subject="email verification",
            message=strip_tags(html),
            html_message=html,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False)
        return Response(newuser, HTTP_201_CREATED)

    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify(request):
    serializer = VerifySerializer(data=request.data)
    if serializer.is_valid():

        data = serializer.validated_data
        ticket = Ticket.objects.filter(ticket=data.get('ticket')).first()
        user = User.objects.filter(id=ticket.user.id).first()
        ticket.user.is_active = True
        ticket.user.save()
        ticket.delete()
        return Response(model_to_dict(user, exclude=["password"]), HTTP_200_OK)

    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentuser(request):
    return Response(model_to_dict(request.user, exclude=["password"]), HTTP_200_OK)


@api_view(['POST'])
def resend(request):
    serializer = ResendSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(email=serializer.validated_data['email'])
        userdata = model_to_dict(user, exclude=["password"])
        maildata = {"ticket": maketicket(user)}
        maildata.update(userdata)
        html = render_to_string('email/verify_email.html', maildata)

        send_mail(
            subject="email verification",
            message=strip_tags(html),
            html_message=html,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email])
        return Response({"detail": "verification resent"}, HTTP_200_OK)
    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def recover(request):

    serializer = RecoverSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(email=serializer.validated_data['email'])
        userdata = model_to_dict(user, exclude=["password"])
        maildata = {"ticket": maketicket(user)}
        maildata.update(userdata)
        html = render_to_string('email/forgot_password.html', maildata)

        send_mail(
            subject="forgot password verification",
            message=strip_tags(html),
            html_message=html,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[serializer.validated_data['email']])

        return Response({"detail": "password reset code sent"}, HTTP_200_OK)

    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset(request):

    serializer = ResetSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        ticket = Ticket.objects.get(ticket=serializer.validated_data['ticket'])
        ticket.user.password = make_password(data['password'])
        ticket.user.save()
        ticket.delete()
        return Response({"detail": "password successfully change"}, HTTP_200_OK)

    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change(request):
    serializer = ChangeSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():

        user = request.user
        user.password = make_password(serializer.validated_data['password'])
        user.save()
        return Response({"detail": "password successfully change"}, HTTP_200_OK)

    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request):

    # Main serializer
    serializer = UpdateSerializer(data=request.data,)

    if serializer.is_valid():

        # update details
        user = request.user
        user.username = serializer.validated_data.get('username')
        user.first_name = serializer.validated_data.get('first_name')
        user.last_name = serializer.validated_data.get('last_name')
        user.save()
        return Response(model_to_dict(user, exclude=["password"]), HTTP_200_OK)

    # respond if not valid
    return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def googleauth(request):

    serializer = GoogleSerializer(data=request.data)
    if serializer.is_valid():

        data = serializer.validated_data['token']
        user = User.objects.filter(email=data['email']).first()
        username = f"{data['first_name']}.{uuid4().hex[:8]}".lower()

        while User.objects.filter(username=username):
            username = f"{data['first_name']}.{uuid4().hex[:8]}".lower()

        if not user:

            new_user = User.objects.create(
                username=username,
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_active=True,
                password=make_password(uuid4().hex[:8])
            )
            user = new_user

        else:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()

        response = model_to_dict(user, exclude=["password"])
        response['access'] = str(maketoken(user))
        return Response(response, HTTP_200_OK)

    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def facebookauth(request):
    serializer = FacebookSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data['token']
        username = ''.join(data.get('first_name').split()).lower()
        user = User.objects.filter(
            email=f"{data.get('id')}@facebook.com").first()

        while User.objects.filter(username=username).first():
            username = username + uuid4().hex[:8]

        if not user:
            new_user = User.objects.create(
                username=username,
                email=f"{data.get('id')}@facebook.com",
                first_name=data['first_name'],
                last_name=data['last_name'],
                is_active=True,
                password=make_password(uuid4().hex[:8])
            )
            user = new_user

        else:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()

        response = model_to_dict(user, exclude=["password"])
        response['access'] = str(maketoken(user))
        return Response(response, HTTP_201_CREATED)

    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def signout(request):
    token = Token.objects.filter(user=request.user)
    token.delete()
    return Response({"detail": "user successfully signout"})
