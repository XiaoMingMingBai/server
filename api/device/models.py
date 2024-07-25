from django.db import models
from django.contrib.auth.models import User  # 导入 User 模型

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')  # 添加外键字段
    # 设备基本信息
    name = models.CharField(max_length=100)
    cpu_name = models.CharField(max_length=100)
    cpu_usage = models.FloatField()
    gpu_name = models.CharField(max_length=100)
    gpu_usage = models.FloatField()
    
    # 私有信息
    func_description = models.TextField(null=True)
    func_usage_cmd = models.TextField(null=True)
    func_usage_params = models.TextField(null=True)
    
    def __str__(self):
        return self.name