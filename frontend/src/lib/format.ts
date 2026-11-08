export function formatDate(iso: string | null | undefined) {
  if (!iso) return "—";
  return new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(new Date(iso));
}

export function useDocumentTitle(title: string) {
  if (typeof document !== "undefined") document.title = `${title} · AI Readiness Assessment`;
}
