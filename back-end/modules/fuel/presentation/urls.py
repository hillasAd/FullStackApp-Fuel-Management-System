from django.urls import path
from .views import (
    VehicleCollectionView, 
    VehicleResourceView,
    FuelRequestCreateView, 
    FuelRequestApproveView,
    FuelRequestRejectView, 
    FuelRequestCancelView, 
    FuelRequestCompleteView,
)

urlpatterns = [
    # --- GESTÃO DE VIATURAS (FROTA) ---
    path('vehicles/', VehicleCollectionView.as_view(), name='vehicle-list-create'),
    path('vehicles/<int:pk>/', VehicleResourceView.as_view(), name='vehicle-detail-update'),

    # --- REQUISIÇÕES V1 (PEDIDOS SIMPLES) ---
    path('requests/', FuelRequestCreateView.as_view(), name='fuel-request-v1-list-create'),
    
    # Ações de Estado v1 (Aprovação, Rejeição, etc)
    path('requests/<int:pk>/approve/', FuelRequestApproveView.as_view(), name='fuel-request-v1-approve'),
    path('requests/<int:pk>/reject/', FuelRequestRejectView.as_view(), name='fuel-request-v1-reject'),
    path('requests/<int:pk>/cancel/', FuelRequestCancelView.as_view(), name='fuel-request-v1-cancel'),
    path('requests/<int:pk>/complete/', FuelRequestCompleteView.as_view(), name='fuel-request-v1-complete'),
]
