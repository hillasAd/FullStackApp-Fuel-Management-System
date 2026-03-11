import { useState } from 'react';
import { useVehicles } from '../../vehicles/hooks/useVehicles';
import { useFuelRequests } from '../hooks/useFuelRequests';
import { Fuel, Plus, Trash2, Send, Info } from 'lucide-react';

const BulkRequestPage = () => {
  const { vehicles } = useVehicles();
  const { createBulkRequest, isCreating } = useFuelRequests();
  
  // Estado local para a "cesta" de abastecimento
  const [items, setItems] = useState([]);
  const [description, setDescription] = useState('');

  // Função para adicionar viatura à lista
  const addItem = (vId) => {
    if (!vId) return;
    const vehicle = vehicles.find(v => v.id === parseInt(vId));
    if (items.find(i => i.vehicle_id === vehicle.id)) return; // Evita duplicados
    
    setItems([...items, { 
      vehicle_id: vehicle.id, 
      license_plate: vehicle.license_plate, 
      model: vehicle.model,
      liters: 10 // Valor padrão inicial
    }]);
  };

  const updateLiters = (index, val) => {
    const newItems = [...items];
    newItems[index].liters = parseFloat(val);
    setItems(newItems);
  };

  const removeItem = (index) => setItems(items.filter((_, i) => i !== index));

  const handleSubmit = () => {
    if (items.length === 0) return;

    createBulkRequest({
      description,
      items: items.map(i => ({ vehicle_id: i.vehicle_id, liters: i.liters }))
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-slate-800 flex items-center">
        <Fuel className="mr-3 text-blue-600" /> Requisição de Lote (v2)
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* COLUNA ESQUERDA: Seleção */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 h-fit">
          <h2 className="font-bold mb-4">Adicionar ao Lote</h2>
          <select 
            onChange={(e) => addItem(e.target.value)}
            className="w-full p-3 rounded-xl border border-slate-300 bg-slate-50 outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Escolher Viatura...</option>
            {vehicles.map(v => (
              <option key={v.id} value={v.id}>{v.license_plate} - {v.model}</option>
            ))}
          </select>
          <p className="text-xs text-slate-400 mt-4">
            <Info className="inline w-3 h-3 mr-1" /> Seleciona as viaturas que farão parte do abastecimento.
          </p>
        </div>

        {/* COLUNA DIREITA: Lista de Itens */}
        <div className="md:col-span-2 space-y-4">
          <input 
            type="text" 
            placeholder="Descrição da Missão (Ex: Escolta Norte)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full p-4 rounded-2xl border-none shadow-sm focus:ring-2 focus:ring-blue-500"
          />

          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            {items.map((item, index) => (
              <div key={item.vehicle_id} className="p-4 flex items-center justify-between border-b border-slate-50 hover:bg-slate-50 transition-colors">
                <div className="flex-1">
                  <div className="font-bold text-blue-700">{item.license_plate}</div>
                  <div className="text-xs text-slate-500">{item.model}</div>
                </div>
                <div className="flex items-center space-x-4">
                  <input 
                    type="number"
                    value={item.liters}
                    onChange={(e) => updateLiters(index, e.target.value)}
                    className="w-20 p-2 border rounded-lg text-center font-bold"
                  />
                  <span className="text-slate-400">L</span>
                  <button onClick={() => removeItem(index)} className="text-red-400 hover:text-red-600 p-2">
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}

            {items.length === 0 && (
              <div className="p-10 text-center text-slate-300">O lote está vazio. Adiciona viaturas à esquerda.</div>
            )}
          </div>

          <button 
            onClick={handleSubmit}
            disabled={items.length === 0 || isCreating}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-2xl shadow-lg transition-all flex justify-center items-center"
          >
            <Send className="w-5 h-5 mr-2" /> SUBMETER LOTE OPERACIONAL
          </button>
        </div>
      </div>
    </div>
  );
};

export default BulkRequestPage;
