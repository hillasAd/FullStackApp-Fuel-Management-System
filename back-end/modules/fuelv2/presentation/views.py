from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from shared.responses.api_response import success, error
from shared.decorator.idempotency import clean_idempotency
from shared.exceptions.custom_exceptions import ConflictException

from ..application.dtos import BulkFuelRequestDTO, FuelItemDTO, ProcessItemDTO
from ..infrastructure.factory import BulkFuelUseCaseFactory
from .serializers import BulkFuelRequestSerializer, BulkActionProcessSerializer

from rest_framework.pagination import PageNumberPagination



class BulkFuelRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @clean_idempotency
    def post(self, request):
        serializer = BulkFuelRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        items_dtos = [
            FuelItemDTO(
                vehicle_id=item['vehicle_id'], 
                liters=item['liters']
            ) for item in request.data.get('items', [])
        ]
        
        dto = BulkFuelRequestDTO(
            requester_id=request.user.id,
            description=request.data.get('description', ''),
            items=items_dtos
        )
        
        use_case = BulkFuelUseCaseFactory.create_bulk_request()
        result = use_case.execute(dto)
        return success(BulkFuelRequestSerializer(result).data, status=201)


class BulkFuelRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Captura os filtros e REMOVE o 'page' para não quebrar o banco
        filters = request.query_params.dict()
        filters.pop('page', None)  # Remove 'page' se existir, sem dar erro se não existir
        
        use_case = BulkFuelUseCaseFactory.create_list_bulk_requests()
        result = use_case.execute(filters=filters)
        
        paginator = PageNumberPagination()
        
        page = paginator.paginate_queryset(result, request, view=self)
        
        if page is not None:
            serializer = BulkFuelRequestSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = BulkFuelRequestSerializer(result, many=True)
        return success(serializer.data)



class BulkFuelRequestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        use_case = BulkFuelUseCaseFactory.create_get_bulk_detail()
        result = use_case.execute(bulk_id=pk)
        if not result:
            return error("Lote não encontrado.", "NOT_FOUND", 404)
        return success(BulkFuelRequestSerializer(result).data)

class BulkFuelItemProcessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, bulk_id, item_id):
        # Captura a versão do header para controle de concorrência
        version = request.data.get('version')
        if version is None:
            return error("A versão do lote é obrigatória.", "VALIDATION_ERROR", 400)

        dto = ProcessItemDTO(
            bulk_id=bulk_id,
            item_id=item_id,
            admin_id=request.user.id,
            action=request.data.get('action'),
            reason=request.data.get('reason'),
            version=int(version)
        )
        try:
            use_case = BulkFuelUseCaseFactory.create_process_bulk_item()
            result_item = use_case.execute(dto)
            return success({"status": result_item.status.value, "item_id": result_item.id})
        except ConflictException as e:
            return error(str(e), "CONFLICT", 409)
        except Exception as e:
            return error(str(e), "BUSINESS_ERROR", 400)
        


class BulkFuelRequestActionView(APIView):
    def post(self, request, pk):
        # 1. Validação com o Serializer correto
        serializer = BulkActionProcessSerializer(data=request.data)
        if not serializer.is_valid():
            return error(serializer.errors, "VALIDATION_ERROR", 400)
        
        data = serializer.validated_data
        
        # 2. Montagem do DTO
        dto = ProcessItemDTO(
            bulk_id=pk,
            item_id=None,
            admin_id=request.user.id,
            action=data['action'],
            reason=data['reason'],
            version=data['version']
        )
        
        try:
            use_case = BulkFuelUseCaseFactory.create_process_bulk_action()
            result_bulk = use_case.execute(dto)
            
            # 3. Retorno
            return success(BulkFuelRequestSerializer(result_bulk).data)
            
        except ConflictException as e:
            return error(str(e), "CONFLICT", 409)
        except Exception as e:
            return error(str(e), "BUSINESS_ERROR", 400)
