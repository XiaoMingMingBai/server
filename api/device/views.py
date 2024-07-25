from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Device
from .serializers import DeviceSerializer,DeviceBelongSerializer, DevicePublicInfoSerializer, DevicePrivateInfoSerializer


class DeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            device = get_object_or_404(Device, id=pk)
            serializer = DeviceBelongSerializer(device)
            return Response(serializer.data)
        devices = Device.objects.all()
        serializer = DeviceBelongSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        device = Device.objects.get(id=pk)
        serializer = DeviceSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, *args, **kwargs):
        device = get_object_or_404(Device, id=pk)
        serializer = DeviceSerializer(device, data=request.data, partial=True)  # 注意这里的partial=True参数
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        device = Device.objects.get(id=pk)
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DevicePublicInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        devices = Device.objects.all()
        serializer = DevicePublicInfoSerializer(devices, many=True)
        return Response(serializer.data)

class DevicePrivateInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        device = Device.objects.get(id=kwargs['pk'])  # 假设通过设备ID访问
        serializer = DevicePrivateInfoSerializer(device)
        return Response(serializer.data)