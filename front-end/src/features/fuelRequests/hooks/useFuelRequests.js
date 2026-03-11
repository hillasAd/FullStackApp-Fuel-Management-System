import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fuelRequestApi } from '../services/fuelRequestApi';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';

// 1. Hook para a Listagem (usado na RequestV2ListPage)
export const useFuelRequests = (page = 1) => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const listQuery = useQuery({ 
    queryKey: ['fuelRequestsV2', page], 
    queryFn: () => fuelRequestApi.listBulk({ page }),
    keepPreviousData: true,
  });

  const createBulkMutation = useMutation({
    mutationFn: (data) => fuelRequestApi.createBulk(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['fuelRequestsV2']);
      Swal.fire('Sucesso!', 'Lote criado.', 'success');
      navigate('/requestsv2');
    }
  });

  return {
    requests: listQuery.data || { results: [], count: 0 },
    isLoadingList: listQuery.isLoading,
    createBulkRequest: createBulkMutation.mutate,
    isCreating: createBulkMutation.isPending,
  };
};

// 2. Hook para o Detalhe e Ações (usado na BulkRequestDetailPage)
export const useFuelRequestDetail = (id) => {
  const queryClient = useQueryClient();

  const detailQuery = useQuery({ 
    queryKey: ['fuelRequestV2', id], 
    queryFn: () => fuelRequestApi.getBulkDetail(id),
    enabled: !!id 
  });

  const invalidate = () => {
    queryClient.invalidateQueries(['fuelRequestsV2']);
    queryClient.invalidateQueries(['fuelRequestV2', id]);
  };

  const itemActionMutation = useMutation({
    mutationFn: ({ itemId, action, version, reason }) => 
      fuelRequestApi.processItem(id, itemId, action, version, reason),
    onSuccess: () => {
      invalidate();
      Swal.fire({ icon: 'success', title: 'Item processado!', timer: 1500, showConfirmButton: false });
    },
    onError: (err) => Swal.fire('Erro', err.response?.data?.message || 'Falha no item', 'error')
  });

  const bulkActionMutation = useMutation({
    mutationFn: ({ action, version, reason }) => 
      fuelRequestApi.processBulkAction(id, action, version, reason),
    onSuccess: () => {
      invalidate();
      Swal.fire('Sucesso!', 'Ação aplicada ao lote.', 'success');
    },
    onError: (err) => Swal.fire('Erro', 'Falha na ação global', 'error')
  });

  return {
    request: detailQuery.data,
    isLoading: detailQuery.isLoading,
    processItem: itemActionMutation.mutate,
    processBulkAction: bulkActionMutation.mutate,
    isProcessing: itemActionMutation.isPending || bulkActionMutation.isPending
  };
};
