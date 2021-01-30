from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=254, required=True)
    name = serializers.CharField(max_length=254, required=True)
    message = serializers.CharField(max_length=5000, required=True)
