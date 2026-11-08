import { cva, type VariantProps } from "class-variance-authority";
import type { ComponentProps } from "react";
import { cn } from "@/lib/utils";

const alertVariants = cva("flex gap-3 rounded-[var(--radius-control)] border p-4 text-sm [&>svg]:mt-0.5 [&>svg]:size-5 [&>svg]:shrink-0", {
  variants: {
    tone: {
      info: "border-blue-600/30 bg-blue-600/5 text-text-primary",
      warning: "border-warning/40 bg-warning/10 text-text-primary",
      danger: "border-danger/40 bg-danger/5 text-danger",
      success: "border-success/40 bg-success/5 text-text-primary",
    },
  },
  defaultVariants: { tone: "info" },
});

export function Alert({
  className,
  tone,
  ...props
}: ComponentProps<"div"> & VariantProps<typeof alertVariants>) {
  return <div className={cn(alertVariants({ tone }), className)} {...props} />;
}
