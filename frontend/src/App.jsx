import { useState, useEffect, useCallback } from "react";
import { Plus, Library } from "lucide-react";
import ResourceCard from "./components/ResourceCard";
import ResourceForm from "./components/ResourceForm";
import Pagination from "./components/Pagination";
import { listResources, createResource, updateResource, deleteResource } from "./api/client";

const PAGE_SIZE = 9;

export default function App() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState(null);

  const fetchResources = useCallback(async (p) => {
    setLoading(true);
    setError(null);
    try {
      const data = await listResources(p, PAGE_SIZE);
      setItems(data.items);
      setTotal(data.total);
    } catch (err) {
      setError("Não foi possível carregar os recursos. Verifique se o backend está rodando.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchResources(page);
  }, [page, fetchResources]);

  const handleSave = async (data) => {
    if (editing) {
      await updateResource(editing.id, data);
    } else {
      await createResource(data);
    }
    setFormOpen(false);
    setEditing(null);
    fetchResources(page);
  };

  const handleDelete = async (resource) => {
    if (!confirm(`Excluir "${resource.title}"?`)) return;
    await deleteResource(resource.id);
    fetchResources(page);
  };

  return (
    <div className="min-h-screen">
      <header className="border-b border-paper-shadow bg-paper/95 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <Library size={22} className="text-archive" />
            <h1 className="font-display text-2xl text-ink">SynapseEdu</h1>
          </div>
          <button
            onClick={() => { setEditing(null); setFormOpen(true); }}
            className="flex items-center gap-2 px-4 py-2 bg-archive text-white text-sm rounded font-medium hover:bg-archive-dark transition-colors"
          >
            <Plus size={16} />
            Novo recurso
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded px-4 py-3 mb-6">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-20 text-ink/50 font-mono text-sm">
            Carregando acervo...
          </div>
        ) : items.length === 0 ? (
          <div className="text-center py-20">
            <p className="font-display text-xl text-ink/60 mb-2">O acervo está vazio</p>
            <p className="text-sm text-ink/40">Cadastre o primeiro recurso educacional.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {items.map((resource) => (
              <ResourceCard
                key={resource.id}
                resource={resource}
                onEdit={(r) => { setEditing(r); setFormOpen(true); }}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}

        {!loading && items.length > 0 && (
          <Pagination page={page} total={total} size={PAGE_SIZE} onPageChange={setPage} />
        )}
      </main>

      {formOpen && (
        <ResourceForm
          initial={editing}
          onSave={handleSave}
          onClose={() => { setFormOpen(false); setEditing(null); }}
        />
      )}
    </div>
  );
}