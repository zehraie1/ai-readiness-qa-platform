import type { ComponentProps } from "react";
import { cn } from "@/lib/utils";

export function Input({ className, ...props }: ComponentProps<"input">) {
  return (
    <input
      className={cn(
        "h-10 w-full rounded-[var(--radius-control)] border border-border bg-surface px-3 text-sm text-text-primary placeholder:text-text-muted aria-[invalid=true]:border-danger",
        className,
      )}
      {...props}
    />
  );
}
