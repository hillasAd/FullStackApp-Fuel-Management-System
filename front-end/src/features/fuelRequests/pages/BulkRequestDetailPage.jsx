import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useFuelRequests, useFuelRequestDetail } from "../hooks/useFuelRequests"; // Usando o hook de detalhe direto
import { useAuth } from "../../../core/auth/useAuth";
import Swal from 'sweetalert2';
import {
  ArrowLeft,
  Check,
  X,
  User,
  Calendar,
  Loader2,
  Send,
} from "lucide-react";
import StatusBadge from "../../../shared/components/ui/StatusBadge";

const BulkRequestDetailPage = () => {
  const { id } = useParams();
  
  const { request, isLoading, processItem, processBulkAction } = useFuelRequestDetail(id);
  
  const [globalAction, setGlobalAction] = useState("");
  const [reason, setReason] = useState("");
  const { isManager, isOperator, isAdmin, user } = useAuth();

  // Validação dinâmica para o botão global
  const isReasonRequired = globalAction === "REJECTED" || globalAction === "CANCELLED";
  const canSubmitGlobal = globalAction && (!isReasonRequired || reason.trim().length > 0);

  // AÇÃO GLOBAL (Lote Completo)
  const handleGlobalSubmit = () => {
    if (isReasonRequired && !reason.trim()) {
        Swal.fire("Atenção", "A justificativa é obrigatória para esta ação.", "warning");
        return;
    }
    
    processBulkAction({
      requestId: id,
      action: globalAction,
      reason: reason,
      version: request.version
    });
    
    setGlobalAction("");
    setReason("");
  };

  // REJEIÇÃO INDIVIDUAL COM PROMPT
  const handleRejectItem = async (itemId) => {
    const { value: text } = await Swal.fire({
      title: 'Justificativa de Rejeição',
      input: 'textarea',
      inputPlaceholder: 'Digite o motivo da rejeição...',
      showCancelButton: true,
      confirmButtonText: 'Rejeitar Viatura',
      confirmButtonColor: '#e11d48',
      inputValidator: (value) => {
        if (!value) return 'Você precisa escrever um motivo!';
      }
    });

    if (text) {
      processItem({
        requestId: id,
        itemId: itemId,
        action: "REJECTED",
        version: request.version,
        reason: text
      });
    }
  };

  if (isLoading)
    return (
      <div className="flex flex-col items-center justify-center h-64">
        <Loader2 className="w-10 h-10 animate-spin text-blue-600 mb-4" />
        <p className="text-slate-500 font-medium">Sincronizando lote operacional...</p>
      </div>
    );

  if (!request) return <div className="p-20 text-center text-red-500 font-bold bg-white rounded-2xl shadow">⚠️ Lote #{id} não encontrado.</div>;

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-in fade-in duration-500">
      <Link to="/requestsv2" className="flex items-center text-slate-500 hover:text-blue-600 transition-colors font-medium">
        <ArrowLeft className="w-4 h-4 mr-2" /> Voltar ao Histórico
      </Link>

      <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-200 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <h1 className="text-3xl font-black text-slate-900 tracking-tight">LOTE #{request.id}</h1>
            <StatusBadge status={request.status} />
          </div>
          <p className="text-slate-600 font-medium italic text-lg leading-relaxed">"{request.description || "Sem observações operacionais"}"</p>
          <div className="flex flex-col space-y-1 text-sm text-slate-500 pt-2">
            <span className="flex items-center"><User size={14} className="mr-1.5" /> Solicitante: {request.requester_id}</span>
            <span className="flex items-center"><Calendar size={14} className="mr-1.5" /> Criado em: {new Date(request.created_at).toLocaleDateString()}</span>
            <span className="font-bold text-blue-600 italic">Versão do Lote: {request.version}</span>
          </div>
        </div>

        {/* AÇÕES GLOBAIS - Só aparecem se NÃO estiver cancelado ou completo */}
        {(isManager || isAdmin || isOperator) && request.status !== "CANCELLED" && request.status !== "COMPLETED" && (
          <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100 space-y-4">
            <h3 className="text-sm font-black text-slate-700 uppercase tracking-wider">Ações em Massa (Lote)</h3>
            <div className="space-y-3">
              <select 
                value={globalAction}
                onChange={(e) => { setGlobalAction(e.target.value); setReason(""); }}
                className="w-full p-3 rounded-xl border-slate-200 text-sm font-medium focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Selecione uma ação...</option>
                {(isManager || isAdmin) && (
                  <>
                    <option value="CANCELLED">Cancelar Lote Completo</option>
                    <option value="APPROVED">Aprovar Todos Itens</option>
                    <option value="REJECTED">Rejeitar Todos Itens</option>
                   <option value="COMPLETED">Finalizar (Abastecer Todos)</option>
                  </>
                )}

              </select>

              {isReasonRequired && (
                <textarea
                  placeholder={`Justificativa obrigatória...`}
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  className="w-full p-3 rounded-xl border-slate-200 text-sm focus:ring-2 focus:ring-rose-500"
                  rows={2}
                />
              )}

              <button
                disabled={!canSubmitGlobal}
                onClick={handleGlobalSubmit}
                className="w-full flex items-center justify-center bg-slate-900 text-white p-3 rounded-xl font-bold hover:bg-blue-600 disabled:bg-slate-200 shadow-md"
              >
                <Send size={16} className="mr-2" /> Executar Ação Global
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="bg-slate-100 border-b border-slate-100">
              <th className="px-8 py-5 text-xs font-black text-slate-600 uppercase tracking-widest">Viatura</th>
              <th className="px-8 py-5 text-xs font-black text-slate-600 uppercase tracking-widest text-center">Quantidade</th>
              <th className="px-8 py-5 text-xs font-black text-slate-600 uppercase tracking-widest text-center">Estado</th>
              <th className="px-8 py-5 text-xs font-black text-slate-600 uppercase tracking-widest text-right">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {request.items.map((item) => (
              <tr key={item.id} className="hover:bg-slate-50/50 transition-colors">
                <td className="px-8 py-5">
                   <span className="font-mono font-bold text-blue-700 text-lg bg-blue-50 px-3 py-1 rounded-lg border border-blue-100">
                      {item.license_plate}
                    </span>
                </td>
                <td className="px-8 py-5 text-center font-black text-slate-700">{item.liters}L</td>
                <td className="px-8 py-5 text-center"><StatusBadge status={item.status} /></td>
                <td className="px-8 py-5 text-right">
                  <div className="flex justify-end space-x-2">
                    {(isManager || isAdmin) && item.status === "PENDING" && (
                      <>
                        <button
                          onClick={() => processItem({ requestId: id, itemId: item.id, action: "APPROVED", version: request.version })}
                          className="p-2.5 bg-emerald-50 text-emerald-600 rounded-xl hover:bg-emerald-100"
                        >
                          <Check size={18} />
                        </button>
                        <button
                          onClick={() => handleRejectItem(item.id)}
                          className="p-2.5 bg-rose-50 text-rose-600 rounded-xl hover:bg-rose-100"
                        >
                          <X size={18} />
                        </button>
                      </>
                    )}
                    {(isOperator || isAdmin) && item.status === "APPROVED" && (
                      <button
                        onClick={() => processItem({ requestId: id, itemId: item.id, action: "FUELED", version: request.version })}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold flex items-center"
                      >
                        <Check size={14} className="mr-1" /> FINALIZAR
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default BulkRequestDetailPage;
