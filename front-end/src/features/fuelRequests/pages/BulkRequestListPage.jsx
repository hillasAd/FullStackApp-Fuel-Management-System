import {
  Eye,
  Fuel,
  Calendar,
  Hash,
  ClipboardList,
  ArrowRight,
  Loader2,
} from "lucide-react";
import { useFuelRequests } from "../hooks/useFuelRequests";
import { Link } from "react-router-dom";
import StatusBadge from "../../../shared/components/ui/StatusBadge";
import Pagination from "../../../shared/components/ui/Pagination";
import { useState } from "react";


const BulkRequestListPage = () => {
  const [page, setPage] = useState(1);
  const { requests, isLoadingList } = useFuelRequests(page);

  if (isLoadingList)
    return (
      <div className="flex flex-col items-center justify-center p-20 animate-pulse">
        <Loader2 className="w-10 h-10 animate-spin text-blue-600 mb-4" />
        <p className="text-slate-400 font-bold uppercase tracking-widest text-xs">
          Sincronizando registros ...
        </p>
      </div>
    );

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in duration-500">
      {/* CABEÇALHO */}
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight flex items-center">
            <ClipboardList className="mr-3 text-blue-600 w-8 h-8" />
            Histórico de Lotes{" "}
            <span className="ml-2 text-blue-600/30 font-mono text-xl">v2</span>
          </h1>
          <p className="text-slate-500 font-medium mt-1">
            Gestão de abastecimentos em massa e missões operacionais.
          </p>
        </div>
        <div className="text-right hidden md:block">
          <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
            Total de Lotes
          </span>
          <div className="text-2xl font-black text-slate-900 leading-none">
            {requests.length}
          </div>
        </div>
      </div>

      {/* TABELA OPERACIONAL */}
      <div className="bg-white rounded-3xl shadow-xl shadow-slate-200/50 border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50 border-b border-slate-100">
                <th className="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest">
                  <div className="flex items-center">
                    <Hash size={12} className="mr-1" /> ID
                  </div>
                </th>
                <th className="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest">
                  Descrição da Missão
                </th>
                <th className="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest">
                  <div className="flex items-center">
                    <Calendar size={12} className="mr-1" /> Data
                  </div>
                </th>
                <th className="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">
                  Estado Global
                </th>
                <th className="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">
                  Ação
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {requests?.results?.map((req) => (
                <tr
                  key={req.id}
                  className="hover:bg-blue-50/30 transition-all group"
                >
                  <td className="px-8 py-5 font-mono font-black text-blue-600 text-lg">
                    #{req.id}
                  </td>
                  <td className="px-8 py-5">
                    <div className="font-bold text-slate-800 text-base leading-tight">
                      {req.description || (
                        <span className="text-slate-300 italic font-normal">
                          Sem descrição informada
                        </span>
                      )}
                    </div>
                    <div className="text-[10px] text-slate-400 mt-1.5 uppercase font-black flex items-center tracking-tighter">
                      <Fuel size={10} className="mr-1 text-slate-300" />{" "}
                      {req.items?.length || 0} Viaturas no lote
                    </div>
                  </td>
                  <td className="px-8 py-5 text-sm font-semibold text-slate-500">
                    {new Date(req.created_at).toLocaleDateString("pt-PT")}
                  </td>
                  <td className="px-8 py-5 text-center">
                    <StatusBadge status={req.status} />
                  </td>
                  <td className="px-8 py-5 text-right">
                    <Link
                      to={`/requests/bulk/${req.id}`}
                      className="inline-flex items-center px-4 py-2 bg-slate-100 text-slate-700 rounded-xl font-black text-[10px] hover:bg-blue-600 hover:text-white transition-all transform group-hover:scale-105 active:scale-95 shadow-sm"
                    >
                      VISUALIZAR <ArrowRight size={14} className="ml-2" />
                    </Link>
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

        {requests.length === 0 && (
          <div className="py-24 text-center">
            <div className="bg-slate-50 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
              <ClipboardList className="w-10 h-10 text-slate-200" />
            </div>
            <p className="text-slate-400 font-bold uppercase text-xs tracking-widest">
              Nenhum lote encontrado.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default BulkRequestListPage;
