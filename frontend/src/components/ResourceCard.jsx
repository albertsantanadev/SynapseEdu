import { Pencil, Trash2, ExternalLink } from "lucide-react";
import TypeBadge from "./TypeBadge";

export default function ResourceCard({ resource, onEdit, onDelete }) {
  return (
    <article className="catalog-notch bg-white border border-paper-shadow rounded-b-lg shadow-sm hover:shadow-md transition-shadow duration-200 flex flex-col">
      <div className="px-5 pt-6 pb-4 flex-1 flex flex-col gap-3">
        <div className="flex items-start justify-between gap-2">
          <TypeBadge type={resource.type} />
          <div className="flex gap-1">
            <button
              onClick={() => onEdit(resource)}
              className="p-1.5 rounded hover:bg-paper-shadow text-ink/60 hover:text-archive transition-colors"
              aria-label="Editar recurso"
            >
              <Pencil size={15} />
            </button>
            <button
              onClick={() => onDelete(resource)}
              className="p-1.5 rounded hover:bg-paper-shadow text-ink/60 hover:text-red-600 transition-colors"
              aria-label="Excluir recurso"
            >
              <Trash2 size={15} />
            </button>
          </div>
        </div>

        <h3 className="font-display text-xl leading-snug text-ink">
          {resource.title}
        </h3>

        <p className="text-sm text-ink/70 leading-relaxed line-clamp-3">
          {resource.description || "Sem descrição — edite para adicionar uma."}
        </p>

        {resource.tags?.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-auto pt-2">
            {resource.tags.map((tag) => (
              <span
                key={tag}
                className="font-mono text-[11px] px-2 py-0.5 bg-paper-shadow rounded text-ink/70"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}
      </div>

      <a
        href={resource.url}
        target="_blank"
        rel="noreferrer"
        className="flex items-center justify-between px-5 py-3 border-t border-paper-shadow text-xs font-mono text-archive hover:bg-archive hover:text-white transition-colors rounded-b-lg"
      >
        Acessar material
        <ExternalLink size={13} />
      </a>
    </article>
  );
}