import { AlertTriangle, Inbox } from "lucide-react";
import type { ReactNode } from "react";
import { isApiError } from "@/api/errors";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

export function PageSkeleton() {
  return (
    <div className="space-y-4 p-6" aria-busy="true">
      <span className="sr-only" role="status">Loading…</span>
      <Skeleton className="h-8 w-64" />
      <Skeleton className="h-32 w-full" />
      <Skeleton className="h-32 w-full" />
    </div>
  );
}

export function ErrorState({ error, onRetry }: { error: unknown; onRetry?: () => void }) {
  const message = error instanceof Error ? error.message : "Something went wrong.";
  const ref = isApiError(error) && error.requestId ? ` (reference ${error.requestId})` : "";
  return (
    <Alert tone="danger" role="alert">
      <AlertTriangle aria-hidden="true" />
      <div className="space-y-2">
        <p>
          {message}
          <span className="text-text-muted">{ref}</span>
        </p>
        {onRetry && (
          <Button variant="outline" size="sm" onClick={onRetry}>
            Try again
          </Button>
        )}
      </div>
    </Alert>
  );
}

export function EmptyState({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div className="flex flex-col items-center gap-3 rounded-[var(--radius-card)] border border-dashed border-border bg-surface p-8 text-center">
      <Inbox aria-hidden="true" className="size-8 text-text-muted" />
      <p className="font-medium">{title}</p>
      {children}
    </div>
  );
}
