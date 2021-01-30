# import from django framework
from django.contrib.auth.hashers import check_password, make_password
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.core.mail import EmailMessage
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
# import from django rest framework
from rest_framework import serializers
# import from this apps
from .utils import checkticket
from .models import Ticket
# import from python
import re


from google.auth.transport import requests
from google.oauth2 import id_token
import facebook

User = get_user_model()


def clean_password(value):
    if len(value) < 8:
        raise serializers.ValidationError(
            'Password must be minimum of 8 characters')

    # check if there is a lowercase character
    if not re.search("[a-z]", value):
        raise serializers.ValidationError(
            'Password must have a lowercase character')

    # check if there is a digit
    if not re.search("[0-9]", value):
        raise serializers.ValidationError(
            'Password must at least have 1 number')

    # check if there is an uppercase character
    if not re.search("[A-Z]", value):
        raise serializers.ValidationError(
            'Password must at least have 1 uppercase character')


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError("Email do not exist")
        return value

    def validate_password(self, value):
        email = self.get_initial()['email']
        user = User.objects.filter(email=email).first()
        if user and not check_password(value, user.password):
            raise serializers.ValidationError('password do not match')
        return value


class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate_password(self, value):
        clean_password(value)
        return value

    def validate_confirm_password(self, value):
        password = self.initial_data['confirm_password']
        if not password:
            return value
        # check if it match the passwordfield
        if password != value:
            raise serializers.ValidationError('password do not match')

        # return valid data
        return value


class VerifySerializer(serializers.Serializer):
    ticket = serializers.CharField(write_only=True, required=True)

    def validate_ticket(self, value):
        # get the request instance
        user = checkticket(value)

        # check if token is valid
        if user is None:
            raise serializers.ValidationError("ticket is invalid")

        if user.is_active == True:
            raise serializers.ValidationError("user is already active")

        # return validated data
        return value


class RecoverSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        # get user instance
        user = User.objects.filter(email=value).first()
        ticket = Ticket.objects.filter(user=user).first()

        if user and ticket:
            countdown = (timezone.now() - ticket.date_created).seconds
            if countdown < 60:
                raise serializers.ValidationError(
                    f"you just sent a request try again after {60-countdown} seconds")

        # check if user exist
        if not user:
            raise serializers.ValidationError("Account doesn't exist")

        # return validated data
        return value


class ResetSerializer(serializers.Serializer):
    ticket = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_ticket(self, value):
        # get the request instance
        ticket = checkticket(value)

        # check if token is valid
        if ticket is None:
            raise serializers.ValidationError("token is invalid")

        # return validated data
        return value

    def validate_password(self, value):
        clean_password(value)
        return value

    def validate_confirm_password(self, value):
        # check if it match the passwordfield
        if self.get_initial()['password'] != value:
            raise serializers.ValidationError('password do not match')

        # return valid data
        return value


class ResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        ticket = Ticket.objects.filter(user=user).first()

        if user and ticket:
            countdown = (timezone.now() - ticket.date_created).seconds
            if countdown < 60:
                raise serializers.ValidationError(
                    f"you just sent a request try again after {60-countdown} seconds")

        if not user:
            raise serializers.ValidationError("Email do not exist")

        if user.is_active:
            raise serializers.ValidationError("user is already active")

        return value


class ChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User

    def validate_old_password(self, value):

        request = self.context.get("request")
        if not check_password(value, request.user.password):
            raise serializers.ValidationError(
                'Wrong password')
        return value

    def validate_password(self, value):
        clean_password(value)
        return value

    def validate_confirm_password(self, value):
        # check if it match the passwordfield
        if self.get_initial()['password'] != value:
            raise serializers.ValidationError('password do not match')

        # return valid data
        return value


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', "first_name", "last_name")


class GoogleSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate_token(self, value):
        # get user instance
        try:
            data = id_token.verify_oauth2_token(value, requests.Request())
        except:
            raise serializers.ValidationError(
                'Token is either invalid or expired')

        if data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise serializers.ValidationError(
                'Token ID not match')

        return {"email": data['email'], "first_name": data['given_name'], "last_name": data['family_name']}


class FacebookSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate_token(self, value):
        # get user instance
        print(value)
        try:
            graph = facebook.GraphAPI(access_token=value)
            data = graph.request('/me?fields=first_name,last_name, email')
        except:
            raise serializers.ValidationError(
                'Token is either invalid or expired')

        return {
            "id": data.get('id'),
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
        }
