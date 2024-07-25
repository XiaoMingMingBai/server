from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'  # 包含所有字段
        
class DeviceBelongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'user')

class DevicePublicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'user', 'cpu_name', 'cpu_usage', 'gpu_name', 'gpu_usage')

class DevicePrivateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('func_description', 'func_usage_cmd', 'func_usage_params')