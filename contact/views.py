from .serializers import ContactSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.core.mail import send_mail
from django.conf import settings


@api_view(['POST'])
def contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        send_mail(
            subject=data['subject'],
            message=f"email: {data['name']}, name: {data['name']}, message: {data['message']}",
            html_message=f"{data['name']} - {data['message']}",
            from_email=data['email'],
            recipient_list=['reilwaystation@gmail.com'],
            fail_silently=False)
        return Response({"detail": "email successfully sent"}, HTTP_200_OK)
    else:
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
