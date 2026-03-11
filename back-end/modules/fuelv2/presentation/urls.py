from django.urls import path
from .views import (
    BulkFuelRequestActionView,
    BulkFuelRequestListView,
    BulkFuelRequestCreateView,
    BulkFuelRequestDetailView,
    BulkFuelItemProcessView
)

app_name = 'fuelv2'

urlpatterns = [
    # --- LISTAGEM E CRIAÇÃO (COLEÇÃO) ---
    path('requests/bulk/', 
         BulkFuelRequestListView.as_view(), 
         name='bulk-request-list'),
    
    # POST: Cria um novo lote completo (Header + Itens)
    path('requests/bulk/create/', 
         BulkFuelRequestCreateView.as_view(), 
         name='bulk-request-create'),
    
    # --- DETALHE DO LOTE (RECURSO) ---
    path('requests/bulk/<int:pk>/', 
         BulkFuelRequestDetailView.as_view(), 
         name='bulk-request-detail'),

    path('requests/bulk/<int:bulk_id>/items/<int:item_id>/process/', 
         BulkFuelItemProcessView.as_view(), 
         name='bulk-item-process'),
    
        # Rota para Ações Globais (Aprovar tudo / Cancelar tudo)
    path('requests/bulk/<int:pk>/process/', 
         BulkFuelRequestActionView.as_view(), 
         name='bulk-request-process'),
]
