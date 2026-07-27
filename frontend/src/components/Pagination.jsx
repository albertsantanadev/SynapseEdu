import { ChevronLeft, ChevronRight } from "lucide-react";

export default function Pagination({ page, total, size, onPageChange }) {
  const totalPages = Math.max(1, Math.ceil(total / size));

  return (
    <div className="flex items-center justify-center gap-4 py-8 font-mono text-sm text-ink/70">
      <button
        onClick={() => onPageChange(page - 1)}
        disabled={page <= 1}
        className="p-2 rounded-full border border-paper-shadow disabled:opacity-30 hover:bg-paper-shadow transition-colors"
        aria-label="Página anterior"
      >
        <ChevronLeft size={16} />
      </button>

      <span>
        página <strong className="text-ink">{page}</strong> de {totalPages}
        <span className="mx-2 text-ink/30">·</span>
        {total} {total === 1 ? "recurso" : "recursos"}
      </span>

      <button
        onClick={() => onPageChange(page + 1)}
        disabled={page >= totalPages}
        className="p-2 rounded-full border border-paper-shadow disabled:opacity-30 hover:bg-paper-shadow transition-colors"
        aria-label="Próxima página"
      >
        <ChevronRight size={16} />
      </button>
    </div>
  );
}