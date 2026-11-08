import { AlertCircle, CheckCircle2, CircleDashed } from "lucide-react";
import { useState } from "react";
import { Link, Navigate, useNavigate, useParams } from "react-router";
import { isApiError } from "@/api/errors";
import { useAttempt, useReview, useSubmitAttempt } from "@/api/queries/assessments";
import { ConfirmSubmitDialog } from "@/components/ConfirmSubmitDialog";
import { ErrorState, PageSkeleton } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { useDocumentTitle } from "@/lib/format";
import { NotFoundPage } from "./NotFoundPage";

export function ReviewPage() {
  useDocumentTitle("Review answers");
  const { id = "" } = useParams();
  const review = useReview(id);
  const attempt = useAttempt(id);
  const submit = useSubmitAttempt(id);
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  if (review.isPending || attempt.isPending) return <PageSkeleton />;
  if (review.isError || attempt.isError) {
    const err = review.error ?? attempt.error;
    return isApiError(err, 404) ? <NotFoundPage /> : <ErrorState error={err} onRetry={() => review.refetch()} />;
  }
  const rv = review.data;
  if (rv.status === "submitted") return <Navigate to={`/attempts/${id}/results`} replace />;

  const unanswered = rv.unanswered_positions.length;
  const onConfirm = () =>
    submit.mutate(undefined, {
      onSuccess: () => navigate(`/attempts/${id}/results`, { replace: true }),
      onError: () => {
        setOpen(false);
        review.refetch();
      },
    });

  return (
    <div className="space-y-6">
      <header>
        <p className="text-sm text-text-muted">{attempt.data.track_name}</p>
        <h1 className="text-2xl font-semibold">Review your answers</h1>
        <p className="mt-1 text-text-muted" data-testid="review-summary">
          {rv.answered} of {rv.total} answered
        </p>
      </header>

      {submit.isError && (
        <Alert tone="danger" role="alert">
          <AlertCircle aria-hidden="true" />
          <p>
            {isApiError(submit.error) && submit.error.code === "ATTEMPT_INCOMPLETE"
              ? "Some questions are still unanswered. Answer them, then submit again."
              : submit.error.message}
          </p>
        </Alert>
      )}

      <Card className="p-0">
        <ol aria-label="Questions" className="divide-y divide-border">
          {rv.items.map((item) => (
            <li key={item.question_id} className="flex items-center justify-between gap-3 px-4 py-3">
              <Link className="font-medium text-blue-700 underline" to={`/attempts/${id}/questions/${item.position}`}>
                Question {item.position}
              </Link>
              {item.answered ? (
                <Badge tone="success">
                  <CheckCircle2 aria-hidden="true" /> Answered
                </Badge>
              ) : (
                <Badge tone="warning">
                  <CircleDashed aria-hidden="true" /> Not answered
                </Badge>
              )}
            </li>
          ))}
        </ol>
      </Card>

      <ConfirmSubmitDialog
        unanswered={unanswered}
        submitting={submit.isPending}
        onConfirm={onConfirm}
        open={open}
        onOpenChange={setOpen}
      />
    </div>
  );
}
