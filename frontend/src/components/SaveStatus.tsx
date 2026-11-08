import { AlertCircle, CheckCircle2, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

export type SaveState = "idle" | "saving" | "saved" | "error";

/** Polite live region so screen readers hear save outcomes without focus moving. */
export function SaveStatus({ state, onRetry }: { state: SaveState; onRetry?: () => void }) {
  return (
    <div aria-live="polite" role="status" className="flex min-h-6 items-center gap-2 text-sm">
      {state === "saving" && (
        <>
          <Loader2 aria-hidden="true" className="size-4 animate-spin" /> Saving answer…
        </>
      )}
      {state === "saved" && (
        <span className="flex items-center gap-2 text-success">
          <CheckCircle2 aria-hidden="true" className="size-4" /> Answer saved
        </span>
      )}
      {state === "error" && (
        <span className="flex items-center gap-2 text-danger">
          <AlertCircle aria-hidden="true" className="size-4" /> Your answer could not be saved.
          {onRetry && (
            <Button variant="link" size="sm" onClick={onRetry}>
              Retry
            </Button>
          )}
        </span>
      )}
    </div>
  );
}
