import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { vehicleApi } from '../services/vehicleApi';
import Swal from 'sweetalert2';

export const useVehicles = () => {
  const queryClient = useQueryClient();

  // Query de Listagem
  const { data: vehicles = [], isLoading, isError } = useQuery({
    queryKey: ['vehicles'],
    queryFn: vehicleApi.list,
    staleTime: 5000,
    refetchInterval: 10000,       // Pergunta ao banco a cada 10 segundos
    refetchIntervalInBackground: true, // Continua a atualizar mesmo se a aba estiver em segundo plano
    refetchOnWindowFocus: true,   // Atualiza assim que o user volta para a aba do sistema
  });

  // Mutation de Criação
  const createMutation = useMutation({
    mutationFn: vehicleApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries(['vehicles']);
      Swal.fire('Sucesso!', 'Viatura registada.', 'success');
    },
    onError: (error) => Swal.fire('Erro!', error.message, 'error'),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => vehicleApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['vehicles']);
      Swal.fire('Atualizado!', 'Dados sincronizados com sucesso.', 'success');
    },
    onError: (error) => Swal.fire('Erro!', error.message, 'error'),
  });

  return {
    vehicles,
    isLoading,
    isError,
    createVehicle: createMutation.mutate,
    isCreating: createMutation.isPending,
    
    // --- EXPORTAR PARA O FORMULÁRIO ---
    updateVehicle: updateMutation.mutate, 
    isUpdating: updateMutation.isPending,
  };
};
