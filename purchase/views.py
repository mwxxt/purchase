from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import *
from .models import Purchase, PurchaseType, LegalAct, ContactInfo
from account.models import Profile
from config import settings
import os
import logging

class PurchaseTypeAPIView(ListAPIView):
    queryset = PurchaseType.objects.all()
    serializer_class = PurchaseTypeSerializer

class PurchaseAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        purchase_objects = Purchase.objects.all().select_related('profile', 'purchase_type').prefetch_related('purchase_additional')
        serializer = PurchaseSerializer(purchase_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        requested_data = request.data
        try:
            profile = Profile.objects.get(user_id=request.user.id)
        except Profile.DoesNotExist:
            return Response({"error":"Профиль не найден"}, status=404)
        requested_data['profile'] = profile.id
        serializer = PurchaseSerializer(data=requested_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        try:
            purchase_object = Purchase.objects.select_related('profile', 'purchase_type').prefetch_related('purchase_additional').get(id=kwargs['pk'])
            serializer = PurchaseSerializer(purchase_object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Purchase.DoesNotExist:
            return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        # logger = logging.getLogger('myapp')
        # logger.setLevel(logging.DEBUG)
        try:
            purchase_instance = Purchase.objects.get(pk=kwargs['pk'])
        except Purchase.DoesNotExist:
            return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseSerializer(instance=purchase_instance, data=request.data, partial=True)
            
        if serializer.is_valid():
            # logger.debug(serializer.validated_data['status_member'])
            for field_name, field_value in request.data.items():
                if field_name in ['documentation', 'contract', 'tech_task', 'instruction']:
                    old_file = getattr(purchase_instance, field_name)
                    if old_file:
                        file_path = os.path.join(settings.MEDIA_ROOT, str(old_file))
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    setattr(purchase_instance, field_name, field_value)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        try:
            purchase_instance = Purchase.objects.get(pk=kwargs['pk'])
        except Purchase.DoesNotExist:
            return Response({"error": "Purchase not found"}, status=status.HTTP_404_NOT_FOUND)

        for field_name in ['documentation', 'contract', 'tech_task', 'instruction']:
            file_field = getattr(purchase_instance, field_name)
            if file_field:
                file_path = os.path.join(settings.MEDIA_ROOT, str(file_field))
                if os.path.exists(file_path):
                    os.remove(file_path)
        purchase_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClosedContractsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Purchase.objects.exclude(winner__isnull=True)
    serializer_class = ClosedPurchaseSerializer


class LegalActListCreate(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = LegalAct.objects.all()
    serializer_class = LegalActSerializer

class LegalActUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = LegalAct.objects.all()
    serializer_class = LegalActSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'file' in request.data:
            old_file = getattr(instance, 'file')
            if old_file:
                file_path = os.path.join(settings.MEDIA_ROOT, str(old_file))
                if os.path.exists(file_path):
                    os.remove(file_path)
            setattr(instance, 'file', request.data.get('file'))
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = getattr(instance, 'file')
        if file_path:
            full_file_path = os.path.join(settings.MEDIA_ROOT, str(file_path))
            if os.path.exists(full_file_path):
                os.remove(full_file_path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactInfoListCreate(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer

class ContactInfoUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer