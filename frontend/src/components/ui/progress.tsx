import { cn } from "@/lib/utils";

export function Progress({ value, max, label, className }: { value: number; max: number; label: string; className?: string }) {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0;
  return (
    <div
      role="progressbar"
      aria-label={label}
      aria-valuemin={0}
      aria-valuemax={max}
      aria-valuenow={value}
      aria-valuetext={`${value} of ${max}`}
      className={cn("h-2 w-full overflow-hidden rounded-full bg-border", className)}
    >
      <div className="h-full bg-blue-600 transition-[width]" style={{ width: `${pct}%` }} />
    </div>
  );
}
