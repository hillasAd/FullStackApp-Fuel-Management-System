import { useState } from "react";
import { useVehicles } from "../hooks/useVehicles";
import VehicleForm from "../components/VehicleForm";
import { Car, Plus, Loader2, Fuel, Edit, AlertCircle, X } from "lucide-react";

const VehicleListPage = () => {
  // 1. ESTADO E DADOS
  const { vehicles, isLoading, isError } = useVehicles();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedVehicle, setSelectedVehicle] = useState(null);

  // 2. HANDLERS
  const handleEdit = (vehicle) => {
    setSelectedVehicle(vehicle);
    setIsModalOpen(true);
  };

  const handleCreate = () => {
    setSelectedVehicle(null); // Limpa para garantir modo "Criação"
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedVehicle(null);
  };

  // 3. ESTADOS DE CARREGAMENTO/ERRO
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h- [400px]">
        <Loader2 className="w-12 h-12 animate-spin text-blue-600 mb-4" />
        <p className="text-slate-500 font-medium">Sincronizando frota ...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="max-w-6xl mx-auto mt-10 bg-red-50 border border-red-200 p-6 rounded-2xl flex items-center text-red-700">
        <AlertCircle className="w-6 h-6 mr-4" />
        <p>Falha ao conectar com o setor de logística. Tente novamente.</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* --- CABEÇALHO --- */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 flex items-center">
            <Car className="mr-3 text-blue-600 w-8 h-8" /> Frota de Viaturas
          </h1>
          <p className="text-slate-500 mt-1">Gerencie os veículos autorizados para abastecimento.</p>
        </div>

        <button
          onClick={handleCreate}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-3 rounded-xl shadow-lg shadow-blue-200 transition-all flex items-center justify-center"
        >
          <Plus className="w-5 h-5 mr-2" /> NOVA VIATURA
        </button>
      </div>

      {/* --- TABELA DE VIATURAS --- */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200">
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Matrícula</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Modelo</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Capacidade</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Combustível</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase text-center">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {vehicles.map((vehicle) => (
                <tr key={vehicle.id} className="hover:bg-slate-50/50 transition-colors group">
                  <td className="px-6 py-4">
                    <span className="font-mono font-bold text-blue-700 bg-blue-50 px-2 py-1 rounded border border-blue-100">
                      {vehicle.license_plate}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm font-semibold text-slate-800">{vehicle.model}</div>
                    <div className="text-xs text-slate-400">ID: #{vehicle.id}</div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center text-sm text-slate-600">
                      <Fuel className="w-4 h-4 mr-2 text-slate-400" />
                      {vehicle.tank_capacity} L
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold ${
                      vehicle.fuel_type === "DIESEL" ? "bg-orange-100 text-orange-700" : "bg-emerald-100 text-emerald-700"
                    }`}>
                      {vehicle.fuel_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    <button
                      onClick={() => handleEdit(vehicle)}
                      className="p-2 opacity-0 group-hover:opacity-100 hover:bg-blue-50 text-blue-600 rounded-lg transition-all"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {vehicles.length === 0 && (
          <div className="py-20 text-center">
            <Car className="w-16 h-16 text-slate-200 mx-auto mb-4" />
            <p className="text-slate-400 font-medium">Nenhuma viatura disponível.</p>
          </div>
        )}
      </div>

      {/* --- MODAL ÚNICO (FORA DA TABELA) --- */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="w-full max-w-lg bg-white rounded-3xl shadow-2xl overflow-hidden animate-in zoom-in-95">
            <div className="p-6 border-b border-slate-100 flex justify-between items-center">
              <h2 className="text-xl font-bold text-slate-800">
                {selectedVehicle ? 'Editar Viatura' : 'Nova Viatura'}
              </h2>
              <button onClick={closeModal} className="text-slate-400 hover:text-slate-600 p-2">
                <X size={20} />
              </button>
            </div>

            <div className="p-8">
              <VehicleForm 
                onSuccess={closeModal} 
                initialData={selectedVehicle} 
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VehicleListPage;
