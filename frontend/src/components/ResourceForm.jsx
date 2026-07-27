import { useState } from "react";
import { X, Sparkles, Loader2 } from "lucide-react";
import { smartAssist } from "../api/client";

const TYPES = ["Vídeo", "PDF", "Link"];

export default function ResourceForm({ initial, onSave, onClose }) {
  const [form, setForm] = useState(
    initial || { title: "", description: "", type: "PDF", url: "", tags: [] }
  );
  const [tagsInput, setTagsInput] = useState(initial?.tags?.join(", ") || "");
  const [aiState, setAiState] = useState("idle"); // idle | loading | error | done
  const [stamped, setStamped] = useState(false);

  const handleChange = (field) => (e) =>
    setForm((f) => ({ ...f, [field]: e.target.value }));

  const handleSmartAssist = async () => {
    if (!form.title.trim()) {
      setAiState("error");
      return;
    }
    setAiState("loading");
    try {
      const result = await smartAssist(form.title, form.type);
      setForm((f) => ({ ...f, description: result.description }));
      setTagsInput(result.tags.join(", "));
      setAiState("done");
      setStamped(true);
      setTimeout(() => setStamped(false), 400);
    } catch (err) {
      setAiState("error");
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const tags = tagsInput
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean)
      .slice(0, 3);
    onSave({ ...form, tags });
  };

  return (
    <div className="fixed inset-0 bg-ink/40 flex items-center justify-center p-4 z-50">
      <div className="bg-paper w-full max-w-lg rounded-lg shadow-xl border border-paper-shadow max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between px-6 py-4 border-b border-paper-shadow">
          <h2 className="font-display text-2xl">
            {initial ? "Editar recurso" : "Novo recurso"}
          </h2>
          <button onClick={onClose} className="text-ink/50 hover:text-ink">
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 flex flex-col gap-4">
          <div>
            <label className="block text-xs font-mono uppercase text-ink/60 mb-1">
              Título *
            </label>
            <input
              required
              value={form.title}
              onChange={handleChange("title")}
              className="w-full border border-paper-shadow rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-archive"
              placeholder="Ex: Introdução a Álgebra Linear"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-mono uppercase text-ink/60 mb-1">
                Tipo *
              </label>
              <select
                value={form.type}
                onChange={handleChange("type")}
                className="w-full border border-paper-shadow rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-archive"
              >
                {TYPES.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-mono uppercase text-ink/60 mb-1">
                URL *
              </label>
              <input
                required
                type="url"
                value={form.url}
                onChange={handleChange("url")}
                className="w-full border border-paper-shadow rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-archive"
                placeholder="https://..."
              />
            </div>
          </div>

          <button
            type="button"
            onClick={handleSmartAssist}
            disabled={aiState === "loading"}
            className={`self-start flex items-center gap-2 px-4 py-2 rounded-full bg-amber text-white text-sm font-medium hover:bg-amber/90 transition-colors disabled:opacity-60 ${stamped ? "animate-stamp" : ""}`}
          >
            {aiState === "loading" ? (
              <Loader2 size={16} className="animate-spin" />
            ) : (
              <Sparkles size={16} />
            )}
            {aiState === "loading" ? "Consultando a IA..." : "Gerar Descrição com IA"}
          </button>

          {aiState === "error" && (
            <p className="text-sm text-red-600 -mt-2">
              Não foi possível gerar a sugestão agora. Preencha manualmente abaixo.
            </p>
          )}

          <div>
            <label className="block text-xs font-mono uppercase text-ink/60 mb-1">
              Descrição
            </label>
            <textarea
              value={form.description}
              onChange={handleChange("description")}
              rows={3}
              className="w-full border border-paper-shadow rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-archive resize-none"
              placeholder="Descrição do material..."
            />
          </div>

          <div>
            <label className="block text-xs font-mono uppercase text-ink/60 mb-1">
              Tags (separadas por vírgula, máx. 3)
            </label>
            <input
              value={tagsInput}
              onChange={(e) => setTagsInput(e.target.value)}
              className="w-full border border-paper-shadow rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-archive"
              placeholder="matematica, algebra, vetores"
            />
          </div>

          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm text-ink/60 hover:text-ink"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-5 py-2 bg-archive text-white text-sm rounded font-medium hover:bg-archive-dark transition-colors"
            >
              Salvar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}