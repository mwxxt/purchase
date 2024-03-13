from rest_framework import serializers
from .models import *
from account.models import Profile
import logging

class PurchaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseType
        fields = "__all__"


class PurchaseAdditionalSerialzier(serializers.ModelSerializer):
    class Meta:
        model = PurchaseAdditional
        fields = "__all__"


class PurchaseMemberSerialzier(serializers.ModelSerializer):
    profile_name = serializers.CharField(source="profile.surname_name", read_only=True)
    class Meta:
        model = PurchaseMember
        fields = ('queue', 'profile', 'profile_name', 'status')


class PurchaseSerializer(serializers.ModelSerializer):
    status_member = serializers.CharField(write_only=True, required=False)
    purchase_additional = PurchaseAdditionalSerialzier(many=True, required=False)
    purchase_members = PurchaseMemberSerialzier(many=True, required=False)
    profile_name = serializers.CharField(source="profile.surname_name", read_only=True)
    purchase_name = serializers.CharField(source="purchase_type.title", read_only=True)
    purchase_type = serializers.PrimaryKeyRelatedField(queryset=PurchaseType.objects.all(), write_only=True)
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), write_only=True)
    date_end = serializers.DateTimeField(format="%d.%m.%Y %H:%M", input_formats=['%d.%m.%Y %H:%M', 'iso-8601'])

    class Meta:
        model = Purchase
        fields = ('id', 'profile', 'profile_name', 'number', 'purchase_type', 'purchase_name', 'title', 'text',
                  'documentation', 'contract', 'tech_task', 'instruction', 'winner', 'date_start', 'date_end', 'purchase_additional', 'status_member', 'purchase_members')

    def create(self, validated_data):
        purchase_additional = validated_data.pop("purchase_additional", [])
        purchase_members = validated_data.pop("purchase_members", [])
        instance = Purchase.objects.create(**validated_data)
        count = 1
        if purchase_additional:
            for obj in purchase_additional:
                PurchaseAdditional.objects.create(purchase=instance, **obj)
        if purchase_members:
            for obj in purchase_members:
                PurchaseMember.objects.create(purchase=instance, queue=count, **obj)
                count += 1
        return instance
    
    def update(self, instance, validated_data):
        purchase_additional = validated_data.pop("purchase_additional", [])
        purchase_members = validated_data.pop("purchase_members", [])
        if purchase_additional:
            for obj in purchase_additional:
                PurchaseAdditional.objects.create(purchase=instance, **obj)
        if purchase_members:
            last = PurchaseMember.objects.filter(purchase=instance).order_by('-queue').first()
            if last is not None:
                queue_number = last.queue + 1
            else:
                queue_number = 1
            for obj in purchase_members:
                PurchaseMember.objects.create(purchase=instance, queue=queue_number, **obj)
                queue_number += 1
        return super(PurchaseSerializer, self).update(instance, validated_data)


class ClosedPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('id', 'number', 'title', 'winner')


class LegalActSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalAct
        fields = "__all__"


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = "__all__"