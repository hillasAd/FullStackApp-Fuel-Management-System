import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Car, Gauge, Loader2, Save, AlertCircle } from 'lucide-react';
import { useVehicles } from '../hooks/useVehicles';

// 1. Esquema de Validação (Incluindo a versão como metadado invisível)
const vehicleSchema = z.object({
  license_plate: z.string()
    .min(5, 'Placa muito curta')
    .max(15, 'Placa muito longa')
    .toUpperCase(),
  model: z.string().min(2, 'Modelo é obrigatório'),
  tank_capacity: z.number()
    .min(1, 'Capacidade deve ser positiva')
    .max(500, 'Capacidade irrealista'),
  fuel_type: z.enum(['DIESEL', 'GASOLINE'], {
    errorMap: () => ({ message: 'Selecione o tipo de combustível' }),
  }),

  version: z.number().optional(),
});

const VehicleForm = ({ onSuccess, initialData }) => {
  const { createVehicle, updateVehicle, isCreating, isUpdating, error } = useVehicles();
  
  const isEditMode = !!initialData;
  const isPending = isCreating || isUpdating;

  // 2. Configuração do Form
  const { register, handleSubmit, reset, formState: { errors } } = useForm({
    resolver: zodResolver(vehicleSchema),
    // No modo edição, o initialData já traz a 'version' do backend
    defaultValues: initialData || { fuel_type: 'DIESEL', version: 1 }
  });

  // Sincroniza o form se o initialData mudar externamente
  useEffect(() => {
    if (initialData) {
      reset(initialData);
    }
  }, [initialData, reset]);

  const onSubmit = (data) => {
    if (isEditMode) {
      // O 'data' aqui já contém a 'version' correta graças ao reset(initialData)
      updateVehicle({ id: initialData.id, data }, {
        onSuccess: (updatedVehicle) => {
          // IMPORTANTE: Atualiza o form com a NOVA versão (ex: v2) 
          // vinda do backend para permitir edições sucessivas sem F5
          reset(updatedVehicle); 
          if (onSuccess) onSuccess();
        }
      });
    } else {
      createVehicle(data, {
        onSuccess: () => {
          reset(); 
          if (onSuccess) onSuccess();
        }
      });
    }
  };

  // 3. Tratamento de Erro de Concorrência (Conflict)
  const isConflict = error?.response?.data?.error?.code === 'conflict';

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
      <header className="mb-4">
        <h3 className="text-lg font-bold text-slate-800 flex items-center">
          {isEditMode ? (
            <><Save className="mr-2 text-blue-600 w-5 h-5" /> Atualizar Viatura</>
          ) : (
            <><Car className="mr-2 text-blue-600 w-5 h-5" /> Nova Viatura</>
          )}
        </h3>
        {isEditMode && (
          <span className="text-xs text-slate-500">Editando: {initialData.license_plate} (Versão: {initialData.version})</span>
        )}
      </header>

      {/* Alerta de Conflito de Versão */}
      {isConflict && (
        <div className="p-3 bg-amber-50 border border-amber-200 rounded-lg flex items-start text-amber-800 text-sm">
          <AlertCircle className="w-5 h-5 mr-2 shrink-0" />
          <p><strong>Atenção:</strong> Outro usuário alterou estes dados. Por favor, recarregue a página para obter a versão mais recente.</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Placa */}
        <div>
          <label className="block text-sm font-medium text-slate-700">Matrícula</label>
          <input
            {...register('license_plate')}
            disabled={isEditMode}
            className={`mt-1 block w-full rounded-lg border p-2 transition-colors ${errors.license_plate ? 'border-red-500' : 'border-slate-300'} ${isEditMode ? 'bg-slate-50 opacity-70' : ''}`}
          />
          {errors.license_plate && <p className="text-red-500 text-xs mt-1">{errors.license_plate.message}</p>}
        </div>

        {/* Modelo */}
        <div>
          <label className="block text-sm font-medium text-slate-700">Modelo</label>
          <input
            {...register('model')}
            className={`mt-1 block w-full rounded-lg border p-2 ${errors.model ? 'border-red-500' : 'border-slate-300'}`}
          />
          {errors.model && <p className="text-red-500 text-xs mt-1">{errors.model.message}</p>}
        </div>

        {/* Capacidade */}
        <div>
          <label className="block text-sm font-medium text-slate-700">Capacidade (L)</label>
          <div className="relative">
             <input
              type="number"
              step="0.1"
              {...register('tank_capacity', { valueAsNumber: true })}
              className={`mt-1 block w-full rounded-lg border p-2 ${errors.tank_capacity ? 'border-red-500' : 'border-slate-300'}`}
            />
            <Gauge className="absolute right-3 top-3 w-4 h-4 text-slate-400" />
          </div>
          {errors.tank_capacity && <p className="text-red-500 text-xs mt-1">{errors.tank_capacity.message}</p>}
        </div>

        {/* Tipo de Combustível */}
        <div>
          <label className="block text-sm font-medium text-slate-700">Combustível</label>
          <select
            {...register('fuel_type')}
            className="mt-1 block w-full rounded-lg border border-slate-300 p-2 bg-white"
          >
            <option value="DIESEL">Diesel</option>
            <option value="GASOLINE">Gasolina</option>
          </select>
        </div>
      </div>

      {/* A versão viaja no state do form mas não tem input visível */}
      <input type="hidden" {...register('version')} />

      <div className="pt-4">
        <button
          type="submit"
          disabled={isPending}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700 transition-all disabled:opacity-50 flex justify-center items-center shadow-md active:scale-95"
        >
          {isPending ? (
            <Loader2 className="w-5 h-5 animate-spin mr-2" />
          ) : isEditMode ? 'GUARDAR ALTERAÇÕES' : 'REGISTAR VIATURA'}
        </button>
      </div>
    </form>
  );
};

export default VehicleForm;
