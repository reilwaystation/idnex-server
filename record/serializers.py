from rest_framework import serializers
from .models import Person, Address, Ownership


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class OwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ownership
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['owner'] = PersonSerializer(instance.owner).data
        response['address'] = AddressSerializer(instance.address).data
        return response
