import { ArrowLeft, ArrowRight, ListChecks } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Link, Navigate, useParams } from "react-router";
import { isApiError } from "@/api/errors";
import { useAttempt, useSaveAnswer } from "@/api/queries/assessments";
import { AssessmentStepper } from "@/components/AssessmentStepper";
import { DraftContentBanner } from "@/components/DraftContentBanner";
import { QuestionCard } from "@/components/QuestionCard";
import { type SaveState, SaveStatus } from "@/components/SaveStatus";
import { ErrorState, PageSkeleton } from "@/components/States";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { useDocumentTitle } from "@/lib/format";
import { NotFoundPage } from "./NotFoundPage";

export function QuestionPage() {
  const { id = "", position = "1" } = useParams();
  const pos = Number(position);
  useDocumentTitle(`Question ${pos}`);
  const attempt = useAttempt(id);
  const save = useSaveAnswer(id);
  // Save status is scoped to the question it belongs to, so navigating resets it to idle.
  const [saveStatus, setSaveStatus] = useState<{ pos: number; state: SaveState }>({ pos, state: "idle" });
  const saveState: SaveState = saveStatus.pos === pos ? saveStatus.state : "idle";
  const setSaveState = (state: SaveState) => setSaveStatus({ pos, state });
  const lastChoice = useRef<{ questionId: string; optionId: string } | null>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);

  // Move focus to the heading when the question changes (announces the new question).
  useEffect(() => {
    headingRef.current?.focus();
  }, [pos]);

  if (attempt.isPending) return <PageSkeleton />;
  if (attempt.isError) {
    if (isApiError(attempt.error, 404)) return <NotFoundPage />;
    return <ErrorState error={attempt.error} onRetry={() => attempt.refetch()} />;
  }
  const a = attempt.data;
  if (a.status === "submitted") return <Navigate to={`/attempts/${a.id}/results`} replace />;
  const question = a.questions[pos - 1];
  if (!Number.isInteger(pos) || !question) return <NotFoundPage />;
  const total = a.total_questions;

  const persist = (choice: { questionId: string; optionId: string }) => {
    lastChoice.current = choice;
    setSaveState("saving");
    save.mutate(choice, {
      onSuccess: () => setSaveState("saved"),
      onError: (e) => {
        setSaveState("error");
        if (isApiError(e, 409)) attempt.refetch();
      },
    });
  };

  return (
    <div className="space-y-6">
      <DraftContentBanner provenance={a.content_provenance} />
      <header className="space-y-3">
        <p className="text-sm text-text-muted">{a.track_name}</p>
        <h1 ref={headingRef} tabIndex={-1} className="text-2xl font-semibold">
          Question {pos} of {total}
        </h1>
        <Progress value={a.answered_count} max={total} label="Questions answered" />
        <p className="text-sm text-text-muted">
          {a.answered_count} of {total} answered
        </p>
      </header>

      <QuestionCard
        question={question}
        total={total}
        onSelect={(optionId) => persist({ questionId: question.question_id, optionId })}
      />
      <SaveStatus state={saveState} onRetry={() => lastChoice.current && persist(lastChoice.current)} />

      <div className="flex flex-wrap items-center justify-between gap-3">
        {pos > 1 ? (
          <Button variant="outline" asChild>
            <Link to={`/attempts/${a.id}/questions/${pos - 1}`}>
              <ArrowLeft aria-hidden="true" /> Previous
            </Link>
          </Button>
        ) : (
          <span />
        )}
        <div className="flex flex-wrap gap-3">
          <Button variant="ghost" asChild>
            <Link to={`/attempts/${a.id}/review`}>
              <ListChecks aria-hidden="true" /> Review answers
            </Link>
          </Button>
          {pos < total ? (
            <Button asChild>
              <Link to={`/attempts/${a.id}/questions/${pos + 1}`}>
                Next <ArrowRight aria-hidden="true" />
              </Link>
            </Button>
          ) : (
            <Button asChild>
              <Link to={`/attempts/${a.id}/review`}>
                Finish and review <ArrowRight aria-hidden="true" />
              </Link>
            </Button>
          )}
        </div>
      </div>

      <AssessmentStepper attemptId={a.id} questions={a.questions} current={pos} />
    </div>
  );
}
