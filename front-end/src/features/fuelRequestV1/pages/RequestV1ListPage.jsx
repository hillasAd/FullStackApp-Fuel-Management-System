import { useFuelRequestV1 } from "../hooks/useFuelRequestV1";
import { useAuth } from "../../../core/auth/useAuth";
import { Fuel, Check, X, Ban, ThumbsUp, Plus } from "lucide-react";
import { useState } from "react";
import RequestV1Form from "../components/RequestV1Form";
import Pagination from "../../../shared/components/ui/Pagination";

const RequestV1ListPage = () => {
  const [page, setPage] = useState(1);
  const {
    requests,
    isLoading,
    approveRequest,
    rejectRequest,
    cancelRequest,
    completeRequest,
  } = useFuelRequestV1(page);

  const { isAdmin, isManager, isOperator, user } = useAuth();
  const [isFormOpen, setIsFormOpen] = useState(false);

  if (isLoading)
    return (
      <div className="p-10 text-center animate-pulse">
        Sincronizando ...
      </div>
    );

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center">
          <Fuel className="mr-3 text-blue-600" /> Requisições v1
        </h1>
        <button
          onClick={() => setIsFormOpen(!isFormOpen)}
          className="bg-blue-600 text-white px-6 py-2 rounded-xl font-bold flex items-center hover:bg-blue-700 transition-all"
        >
          {isFormOpen ? <X className="mr-2" /> : <Plus className="mr-2" />}
          {isFormOpen ? "FECHAR" : "NOVO PEDIDO"}
        </button>
      </div>

      {isFormOpen && <RequestV1Form onSuccess={() => setIsFormOpen(false)} />}

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">
                Viatura
              </th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">
                Litros
              </th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">
                Estado
              </th>
              <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase text-center">
                Ações
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {requests?.results?.map((req) => (
              <tr key={req.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4">
                  <div className="font-bold text-slate-800">
                    {req.vehicle.license_plate}
                  </div>
                  <div className="text-xs text-slate-400">
                    {req.vehicle.model}
                  </div>
                </td>
                <td className="px-6 py-4 font-mono font-bold text-slate-700">
                  {req.liters}L
                </td>
                <td className="px-6 py-4">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-bold ${
                      req.status === "PENDING"
                        ? "bg-amber-100 text-amber-700"
                        : req.status === "APPROVED"
                          ? "bg-blue-100 text-blue-700"
                          : req.status === "FUELED"
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                    }`}
                  >
                    {req.status}
                  </span>
                </td>
                <td className="px-6 py-4 flex justify-center space-x-2">
                  {/* Ações do Manager */}
                  {isManager && req.status === "PENDING" && (
                    <>
                      <button
                        onClick={() => approveRequest(req.id)}
                        className="p-2 bg-green-50 text-green-600 rounded-lg hover:bg-green-100"
                        title="Aprovar"
                      >
                        <ThumbsUp size={18} />
                      </button>
                      <button
                        onClick={() => rejectRequest(req.id)}
                        className="p-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100"
                        title="Rejeitar"
                      >
                        <Ban size={18} />
                      </button>
                    </>
                  )}
                  {/* Ações do Condutor (Dono do pedido) */}
                  {req.requester_id === user?.id &&
                    req.status === "PENDING" && (
                      <button
                        onClick={() => cancelRequest(req.id)}
                        className="text-xs font-bold text-red-500 hover:underline"
                      >
                        Cancelar
                      </button>
                    )}

                  {/* Ação do Operador: Só aparece se estiver APROVADO e for OPERADOR ou ADMIN */}
                  {(isOperator) && req.status === "APPROVED" && (
                    <button
                      onClick={() => completeRequest(req.id)}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold flex items-center transition-colors"
                    >
                      <Check size={14} className="mr-1" /> FINALIZAR
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <Pagination
          count={requests?.count}
          currentPage={page}
          onPageChange={(p) => setPage(p)}
          pageSize={15} 
        />
      </div>
    </div>
  );
};

export default RequestV1ListPage;
