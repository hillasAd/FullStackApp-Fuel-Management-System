import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fuelRequestV1Api } from '../services/fuelRequestV1Api';
import Swal from 'sweetalert2';

export const useFuelRequestV1 = (page = 1) => {
  const queryClient = useQueryClient();

  // 1. Query com suporte a paginação
  const { data, isLoading } = useQuery({
    queryKey: ['fuelRequestsV1', page], 
    queryFn: () => fuelRequestV1Api.list({ page }),
    keepPreviousData: true, // Mantém a página anterior enquanto carrega a nova (evita flicker)
  });

  // 2. Helper de Mutação Corrigido (useMutation não pode estar dentro de outra função)
  const createMutation = useMutation({
    mutationFn: fuelRequestV1Api.create,
    onSuccess: () => {
      queryClient.invalidateQueries(['fuelRequestsV1']);
      Swal.fire('Sucesso!', 'Pedido criado.', 'success');
    },
    onError: (err) => Swal.fire('Erro', err.message, 'error')
  });

  const approveMutation = useMutation({
    mutationFn: fuelRequestV1Api.approve,
    onSuccess: () => {
      queryClient.invalidateQueries(['fuelRequestsV1']);
      Swal.fire('Sucesso!', 'Pedido aprovado.', 'success');
    }
  });

  const rejectMutation = useMutation({
    mutationFn: fuelRequestV1Api.reject,
    onSuccess: () => {
      queryClient.invalidateQueries(['fuelRequestsV1']);
      Swal.fire('Sucesso!', 'Pedido rejeitado.', 'success');
    }
  });

  const cancelMutation = useMutation({
    mutationFn: fuelRequestV1Api.cancel,
    onSuccess: () => {
      queryClient.invalidateQueries(['fuelRequestsV1']);
      Swal.fire('Sucesso!', 'Pedido cancelado.', 'success');
    }
  });

  const completeMutation = useMutation({
    mutationFn: fuelRequestV1Api.complete,
    onSuccess: () => {
      queryClient.invalidateQueries(['fuelRequestsV1']);
      Swal.fire('Sucesso!', 'Abastecimento concluído.', 'success');
    }
  });

  return {

    requests: data || { results: [], count: 0 }, 
    isLoading,
    createRequest: createMutation.mutate,
    approveRequest: approveMutation.mutate,
    rejectRequest: rejectMutation.mutate,
    cancelRequest: cancelMutation.mutate,
    completeRequest: completeMutation.mutate,
    // Status de carregamento global para ações
    isProcessing: 
      createMutation.isPending || 
      approveMutation.isPending || 
      rejectMutation.isPending || 
      cancelMutation.isPending || 
      completeMutation.isPending
  };
};
