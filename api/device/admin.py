from django.contrib import admin
from .models import Device  # 假设 Device 模型在 models.py 文件中定义

# 在这里注册您的模型
admin.site.register(Device)