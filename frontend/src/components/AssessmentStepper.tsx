import { Check } from "lucide-react";
import { Link } from "react-router";
import type { AttemptQuestion } from "@/api/types";
import { cn } from "@/lib/utils";

/** 20-cell navigator. Answered state uses icon + accessible text, not colour alone. */
export function AssessmentStepper({
  attemptId,
  questions,
  current,
}: {
  attemptId: string;
  questions: AttemptQuestion[];
  current: number;
}) {
  return (
    <nav aria-label="Question navigator">
      <ol className="grid grid-cols-10 gap-1.5">
        {questions.map((q) => {
          const answered = q.selected_option_id != null;
          const isCurrent = q.position === current;
          return (
            <li key={q.question_id}>
              <Link
                to={`/attempts/${attemptId}/questions/${q.position}`}
                aria-current={isCurrent ? "step" : undefined}
                aria-label={`Question ${q.position}, ${answered ? "answered" : "not answered"}`}
                className={cn(
                  "flex h-9 items-center justify-center rounded-md border text-xs font-medium",
                  answered ? "border-blue-600 bg-blue-600/10 text-blue-700" : "border-border bg-surface",
                  isCurrent && "ring-2 ring-navy-900",
                )}
              >
                {answered ? <Check aria-hidden="true" className="size-3.5" /> : q.position}
              </Link>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
