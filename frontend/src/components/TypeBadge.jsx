import { Video, FileText, Link2 } from "lucide-react";

const CONFIG = {
  "Vídeo": { icon: Video, color: "text-archive", bg: "bg-archive/10" },
  "PDF": { icon: FileText, color: "text-amber", bg: "bg-amber/10" },
  "Link": { icon: Link2, color: "text-moss", bg: "bg-moss/10" },
};

export default function TypeBadge({ type }) {
  const { icon: Icon, color, bg } = CONFIG[type] || CONFIG["Link"];
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full font-mono text-xs uppercase tracking-wide ${color} ${bg}`}
    >
      <Icon size={13} strokeWidth={2.2} />
      {type}
    </span>
  );
}