from django.urls import path
from .views import DeviceView, DevicePublicInfoView, DevicePrivateInfoView

urlpatterns = [
    path('devices/public/', DevicePublicInfoView.as_view(), name='device-public-info'),
    path('devices/<int:pk>/private/', DevicePrivateInfoView.as_view(), name='device-private-info'),
    path('devices/', DeviceView.as_view(), name='device-list-create'),
    path('devices/<int:pk>/', DeviceView.as_view(), name='device-detail-update-delete'),
]