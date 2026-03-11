from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from modules.fuel.infrastructure.factory import FuelRequestUseCaseFactory, VehicleUseCaseFactory
from shared.exceptions.custom_exceptions import ConflictException, NotFoundException
from shared.responses.api_response import success, error

from .permissions import IsManager, IsOperator
from .serializers import (
    VehicleSerializer, FuelRequestSerializer, 
)

# Novas Factories Separadas
from ..application.dtos import VehicleDTO, FuelRequestDTO
from rest_framework.pagination import PageNumberPagination


# ==============================================================================
# GESTÃO DE VIATURAS (VEHICLE FACTORY)
# ==============================================================================

class VehicleCollectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        use_case = VehicleUseCaseFactory.create_get_vehicle()
        vehicles = use_case.execute_list()
        return success(VehicleSerializer(vehicles, many=True).data)

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case = VehicleUseCaseFactory.create_register_vehicle()
        vehicle = use_case.execute(VehicleDTO(**serializer.validated_data))
        return success(VehicleSerializer(vehicle).data, status=201)

class VehicleResourceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        use_case = VehicleUseCaseFactory.create_get_vehicle() 
        vehicle = use_case.execute_detail(vehicle_id=pk)
        if not vehicle:
            return error("Viatura não encontrada.", "NOT_FOUND", 404)
        return success(VehicleSerializer(vehicle).data)
        
    def put(self, request, pk):
        raw_version = request.data.get("version")
        if raw_version is None:
            return error("Version is required for optimistic concurrency.", "VALIDATION_ERROR", 400)
        
        serializer = VehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        dto = VehicleDTO(**serializer.validated_data, version=int(raw_version))
        
        try:
            use_case = VehicleUseCaseFactory.create_update_vehicle()
            vehicle = use_case.execute(vehicle_id=pk, dto=dto)
            return success(VehicleSerializer(vehicle).data)
        except ConflictException as e:
            return error(str(e), "CONFLICT", 409)
        except NotFoundException as e:
            return error(str(e), "NOT_FOUND", 404)

# ==============================================================================
# REQUISIÇÕES V1 (FUEL REQUEST FACTORY)
# ==============================================================================

class FuelRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'burst'

    def get(self, request):
        use_case = FuelRequestUseCaseFactory.create_list_fuel_requests()
        filters = {} if request.user.role in ['MANAGER', 'ADMIN'] else {'requester_id': request.user.id}
        requests = use_case.execute(filters=filters)
        
        paginator = PageNumberPagination()
        # 1. Pagina o queryset ou lista
        page = paginator.paginate_queryset(requests, request)
        
        if page is not None:
            serializer = FuelRequestSerializer(page, many=True)
            # 2. Retorna via get_paginated_response para incluir 'next', 'previous' e 'count'
            return paginator.get_paginated_response(serializer.data)

        # Fallback caso a paginação falhe ou não seja aplicada
        serializer = FuelRequestSerializer(requests, many=True)
        return success(serializer.data)

    def post(self, request):
        serializer = FuelRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = FuelRequestDTO(
            vehicle_id=serializer.validated_data['vehicle_id'],
            liters=serializer.validated_data['amount']['liters'],
            requester_id=request.user.id
        )
        use_case = FuelRequestUseCaseFactory.create_request_fuel()
        result = use_case.execute(dto)
        return success(FuelRequestSerializer(result).data, status=201)

class FuelRequestApproveView(APIView):
    permission_classes = [IsAuthenticated, IsManager]
    def post(self, request, pk):
        use_case = FuelRequestUseCaseFactory.create_approve_fuel()
        result = use_case.execute(request_id=pk, admin_id=request.user.id)
        return success(FuelRequestSerializer(result).data)


class FuelRequestRejectView(APIView):
    """Rejeição de um pedido individual (V1)"""
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, pk):
        # 1. Instanciar o Use Case via Factory
        use_case = FuelRequestUseCaseFactory.create_reject_fuel()
        
        # 2. Executar (Passando ID do pedido e ID do administrador que rejeita)
        result = use_case.execute(
            request_id=pk, 
            admin_id=request.user.id
        )
        
        return success(FuelRequestSerializer(result).data)


class FuelRequestCancelView(APIView):
    """Cancelamento pelo próprio requerente (V1)"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        use_case = FuelRequestUseCaseFactory.create_cancel_fuel()
        
        # O Use Case valida se o request.user.id é o dono do pedido
        result = use_case.execute(
            request_id=pk, 
            user_id=request.user.id
        )
        
        return success(FuelRequestSerializer(result).data)


class FuelRequestCompleteView(APIView):
    """Finalização do abastecimento pelo frentista/operador (V1)"""
    permission_classes = [IsAuthenticated, IsOperator]

    def post(self, request, pk):
        use_case = FuelRequestUseCaseFactory.create_fueling_completed()
        
        # O Operador confirma que o combustível foi colocado na viatura
        result = use_case.execute(
            request_id=pk, 
            operator_id=request.user.id
        )
        
        return success(FuelRequestSerializer(result).data)