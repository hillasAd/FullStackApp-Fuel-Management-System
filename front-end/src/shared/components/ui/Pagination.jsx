export default function Pagination({ count, currentPage, onPageChange, pageSize = 15 }) {
  const totalPages = Math.ceil(count / pageSize);

  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-between p-4 bg-white border-t border-slate-100">
      <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
        Página {currentPage} de {totalPages} • Total: {count}
      </span>
      <div className="flex gap-2">
        <button
          disabled={currentPage === 1}
          onClick={() => onPageChange(currentPage - 1)}
          className="px-4 py-2 bg-slate-50 text-slate-600 rounded-xl text-[10px] font-black uppercase hover:bg-slate-100 disabled:opacity-30 transition-all"
        >
          Anterior
        </button>
        <button
          disabled={currentPage === totalPages}
          onClick={() => onPageChange(currentPage + 1)}
          className="px-4 py-2 bg-slate-900 text-white rounded-xl text-[10px] font-black uppercase hover:bg-slate-800 disabled:opacity-30 transition-all"
        >
          Próximo
        </button>
      </div>
    </div>
  );
}
