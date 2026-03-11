const StatusBadge = ({ status }) => {
  const configs = {
    PENDING: {
      color: "bg-amber-100 text-amber-700 border-amber-200",
      label: "Pendente",
    },
    APPROVED: {
      color: "bg-blue-100 text-blue-700 border-blue-200",
      label: "Aprovado",
    },
    REJECTED: {
      color: "bg-red-100 text-red-700 border-red-200",
      label: "Rejeitado",
    },
    CANCELLED: {
      color: "bg-slate-100 text-slate-700 border-slate-200",
      label: "Cancelado",
    },
    PROCESSED: {
      color: "bg-indigo-100 text-indigo-700 border-indigo-200",
      label: "Em Processamento",
    },
    FUELED: {
      color: "bg-emerald-100 text-emerald-700 border-emerald-200",
      label: "Abastecido",
    },
    COMPLETED: {
      color: "bg-green-100 text-green-700 border-green-200",
      label: "Concluído",
    },
    CONFIRMED: {
      color: "bg-purple-100 text-purple-700 border-purple-200",
      label: "Confirmado",
    },
  };

  // Se o status não existir no mapeamento, exibe o texto bruto para facilitar o debug
  const config = configs[status] || {
    color: "bg-gray-100 text-gray-600 border-gray-200",
    label: status || "N/A",
  };

  return (
    <span
      className={`px-3 py-1 rounded-full text-[10px] font-bold border ${config.color} whitespace-nowrap`}
    >
      {config.label.toUpperCase()}
    </span>
  );
};

export default StatusBadge;
