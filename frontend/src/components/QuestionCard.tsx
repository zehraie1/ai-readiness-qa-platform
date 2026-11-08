import { useId } from "react";
import type { AttemptQuestion } from "@/api/types";
import { Card } from "@/components/ui/card";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { cn } from "@/lib/utils";

interface Props {
  question: AttemptQuestion;
  total: number;
  disabled?: boolean;
  onSelect: (optionId: string) => void;
}

/** One question per view. Radix RadioGroup gives arrow-key selection and roving focus. */
export function QuestionCard({ question, total, disabled, onSelect }: Props) {
  const legendId = useId();
  return (
    <Card>
      <fieldset aria-labelledby={legendId}>
        <p className="text-xs font-semibold uppercase tracking-wide text-text-muted">
          {question.category === "common" ? "Common question" : "Track question"} · Question{" "}
          {question.position} of {total}
        </p>
        <legend id={legendId} className="mt-2 text-lg font-semibold leading-snug">
          {question.prompt}
        </legend>
        <RadioGroup
          className="mt-5"
          aria-labelledby={legendId}
          value={question.selected_option_id ?? ""}
          onValueChange={onSelect}
          disabled={disabled}
        >
          {question.options.map((o) => {
            const id = `${legendId}-${o.id}`;
            const selected = question.selected_option_id === o.id;
            return (
              <label
                key={o.id}
                htmlFor={id}
                className={cn(
                  "flex cursor-pointer items-start gap-3 rounded-[var(--radius-control)] border border-border p-4 hover:bg-canvas",
                  selected && "border-blue-600 bg-blue-600/5",
                )}
              >
                <RadioGroupItem id={id} value={o.id} />
                <span>
                  <span className="font-semibold">{o.id}.</span> {o.text}
                </span>
              </label>
            );
          })}
        </RadioGroup>
      </fieldset>
    </Card>
  );
}
