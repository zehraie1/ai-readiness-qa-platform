import { useState } from "react";
import { useNavigate } from "react-router";
import { useStartAttempt, useTracks } from "@/api/queries/assessments";
import type { Track } from "@/api/types";
import { DraftContentBanner } from "@/components/DraftContentBanner";
import { ErrorState, PageSkeleton } from "@/components/States";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogTitle,
} from "@/components/ui/dialog";
import { useDocumentTitle } from "@/lib/format";

export function TracksPage() {
  useDocumentTitle("Choose an assessment");
  const tracks = useTracks();
  const start = useStartAttempt();
  const navigate = useNavigate();
  const [selected, setSelected] = useState<Track | null>(null);

  if (tracks.isPending) return <PageSkeleton />;
  if (tracks.isError) return <ErrorState error={tracks.error} onRetry={() => tracks.refetch()} />;

  const begin = () => {
    if (!selected) return;
    start.mutate(selected.id, {
      onSuccess: (attempt) => {
        const first = attempt.questions.find((q) => !q.selected_option_id)?.position;
        navigate(first ? `/attempts/${attempt.id}/questions/${first}` : `/attempts/${attempt.id}/review`);
      },
    });
  };

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">Choose an assessment track</h1>
        <p className="mt-1 text-text-muted">
          Each assessment has 20 questions: 10 common questions and 10 for your selected track.
        </p>
      </header>
      <DraftContentBanner provenance={tracks.data[0]?.content_provenance} />
      <ul className="grid gap-4 sm:grid-cols-2">
        {tracks.data.map((t) => (
          <li key={t.id}>
            <Card className="flex h-full flex-col gap-3">
              <h2 className="text-lg font-semibold">{t.name}</h2>
              <p className="flex-1 text-sm text-text-muted">{t.description}</p>
              <p className="text-sm">{t.question_count} questions</p>
              <Button className="self-start" disabled={!t.available} onClick={() => setSelected(t)}>
                Start <span className="sr-only">{t.name}</span>
              </Button>
            </Card>
          </li>
        ))}
      </ul>

      <Dialog open={selected !== null} onOpenChange={(o) => !o && setSelected(null)}>
        <DialogContent>
          <DialogTitle>Start {selected?.name}</DialogTitle>
          <DialogDescription>Before you begin:</DialogDescription>
          <ul className="mt-3 list-disc space-y-1 pl-5 text-sm">
            <li>There are 20 multiple-choice questions, each with one correct answer.</li>
            <li>Questions appear one at a time in a fixed order.</li>
            <li>Your answers are saved automatically. You can leave and resume later.</li>
            <li>All 20 questions must be answered before you can submit.</li>
            <li>Submitted answers are final. You may retake the track later.</li>
          </ul>
          {start.isError && <div className="mt-4"><ErrorState error={start.error} /></div>}
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline">Cancel</Button>
            </DialogClose>
            <Button onClick={begin} disabled={start.isPending}>
              {start.isPending ? "Starting…" : "Begin assessment"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
