from django.urls import path
from . import views_revolutionary

urlpatterns = [
    path('visual-search/', views_revolutionary.visual_search, name='visual_search'),
    path('supply-chain/track/', views_revolutionary.track_supply_chain, name='track_supply_chain'),
    path('authenticity/<str:product_id>/', views_revolutionary.verify_authenticity, name='verify_authenticity'),
    path('iot/register/', views_revolutionary.register_iot_device, name='register_iot_device'),
    path('iot/status/<str:device_id>/', views_revolutionary.iot_device_status, name='iot_device_status'),
    path('supply-chain/history/<str:product_id>/', views_revolutionary.supply_chain_history, name='supply_chain_history'),
]