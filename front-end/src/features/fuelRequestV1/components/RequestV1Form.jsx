import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useFuelRequestV1 } from '../hooks/useFuelRequestV1';
import { useVehicles } from '../../vehicles/hooks/useVehicles';
import { Loader2 } from 'lucide-react';

// 1. Esquema de Validação Único e Robusto
const schema = z.object({
  vehicle_id: z.string().min(1, 'Selecione uma viatura'),
  liters: z.number({ invalid_type_error: 'Introduza um número' })
    .positive('Deve ser maior que zero')
    .max(200, 'Máximo permitido é 200L'),
});

const RequestV1Form = ({ onSuccess }) => {
  const { createRequest, isProcessing } = useFuelRequestV1();
  const { vehicles } = useVehicles();
  
  const { register, handleSubmit, formState: { errors } } = useForm({ 
    resolver: zodResolver(schema) 
  });

  const onSubmit = (data) => {
    // 2. Ponte para o DTO do Backend
    createRequest(
      { ...data, vehicle_id: parseInt(data.vehicle_id) }, 
      { onSuccess }
    );
  };

  return (
    <form 
      onSubmit={handleSubmit(onSubmit)} 
      className="bg-slate-50 p-6 rounded-2xl border-2 border-dashed border-slate-200 grid grid-cols-1 md:grid-cols-3 gap-4 items-start"
    >
      {/* Seleção de Viatura */}
      <div className="flex flex-col">
        <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">Viatura</label>
        <select 
          {...register('vehicle_id')} 
          className={`w-full p-2 rounded-lg border ${errors.vehicle_id ? 'border-red-500' : 'border-slate-300'} bg-white`}
        >
          <option value="">Selecionar...</option>
          {vehicles.map(v => (
            <option key={v.id} value={v.id}>{v.license_plate} - {v.model}</option>
          ))}
        </select>
        {errors.vehicle_id && <span className="text-red-500 text-[10px] mt-1 font-bold">{errors.vehicle_id.message}</span>}
      </div>

      {/* Input de Litros */}
      <div className="flex flex-col">
        <label className="block text-[10px] font-bold text-slate-500 uppercase mb-1">Litros</label>
        <input 
          name="liters"
          type="number" 
          step="0.1"
          {...register('liters', { valueAsNumber: true })} 
          className={`w-full p-2 rounded-lg border ${errors.liters ? 'border-red-500' : 'border-slate-300'} bg-white`}
          placeholder="Ex: 50"
        />
        {errors.liters && <span className="text-red-500 text-[10px] mt-1 font-bold">{errors.liters.message}</span>}
      </div>

      {/* Botão de Submissão */}
      <div className="h-full flex items-end">
        <button 
          type="submit" 
          disabled={isProcessing}
          className="w-full bg-blue-600 text-white p-2.5 rounded-lg font-bold hover:bg-blue-800 transition-all disabled:opacity-50 flex justify-center items-center h- [42px]"
        >
          {isProcessing ? <Loader2 className="animate-spin w-5 h-5" /> : 'SOLICITAR ABASTECIMENTO'}
        </button>
      </div>
    </form>
  );
};

export default RequestV1Form;
