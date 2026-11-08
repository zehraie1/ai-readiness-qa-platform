import { ArrowRight, CheckCircle2, CircleDashed, PlayCircle, RotateCcw } from "lucide-react";
import { Link } from "react-router";
import { useMe } from "@/api/queries/auth";
import { useDashboardSummary } from "@/api/queries/assessments";
import type { TrackStatus } from "@/api/types";
import { ChartFigure, ColumnChart, DataTable, PercentBarChart } from "@/components/charts";
import { DraftContentBanner } from "@/components/DraftContentBanner";
import { EmptyState, ErrorState, PageSkeleton } from "@/components/States";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { BAND_LABEL } from "@/lib/bands";
import { cn } from "@/lib/utils";
import { formatDate, useDocumentTitle } from "@/lib/format";

function TrackCard({ t }: { t: TrackStatus }) {
  return (
    <Card
      className={cn(
        "flex h-full flex-col gap-3 border-t-4",
        t.status === "completed"
          ? "border-t-success"
          : t.status === "in_progress"
            ? "border-t-blue-600"
            : "border-t-border",
      )}
    >
      <div className="flex items-start justify-between gap-2">
        <h3 className="text-lg font-semibold text-navy-900">{t.track_name}</h3>
        {t.status === "in_progress" && (
          <Badge tone="info">
            <CircleDashed aria-hidden="true" /> In progress
          </Badge>
        )}
        {t.status === "completed" && (
          <Badge tone="success">
            <CheckCircle2 aria-hidden="true" /> Completed
          </Badge>
        )}
        {t.status === "not_started" && <Badge tone="neutral">Not started</Badge>}
      </div>
      <p className="flex-1 text-sm text-text-muted">
        {t.status === "in_progress" && `${t.answered_count} of 20 answered`}
        {t.status !== "in_progress" &&
          t.attempts_completed > 0 &&
          `Latest ${t.latest_score}/100 (${BAND_LABEL[t.latest_band ?? ""] ?? "—"}) · best ${t.best_score}/100 · ${t.attempts_completed} completed`}
        {t.status === "not_started" && "No attempts yet."}
        {t.status === "in_progress" && t.attempts_completed > 0 && ` · best ${t.best_score}/100`}
      </p>
      <div className="flex flex-wrap gap-2">
        {t.status === "in_progress" && t.in_progress_attempt_id && (
          <Button asChild>
            <Link
              to={
                t.resume_position
                  ? `/attempts/${t.in_progress_attempt_id}/questions/${t.resume_position}`
                  : `/attempts/${t.in_progress_attempt_id}/review`
              }
            >
              Resume <span className="sr-only">{t.track_name} assessment</span>
              <ArrowRight aria-hidden="true" />
            </Link>
          </Button>
        )}
        {t.status === "not_started" && (
          <Button asChild variant="outline">
            <Link to="/assessments/tracks">
              <PlayCircle aria-hidden="true" /> Start{" "}
              <span className="sr-only">{t.track_name}</span>
            </Link>
          </Button>
        )}
        {t.latest_attempt_id && (
          <Button asChild variant="outline">
            <Link to={`/attempts/${t.latest_attempt_id}/results`}>
              View latest results <span className="sr-only">for {t.track_name}</span>
            </Link>
          </Button>
        )}
        {t.status === "completed" && (
          <Button asChild variant="ghost">
            <Link to="/assessments/tracks">
              <RotateCcw aria-hidden="true" /> Retake{" "}
              <span className="sr-only">{t.track_name}</span>
            </Link>
          </Button>
        )}
      </div>
    </Card>
  );
}

export function DashboardPage() {
  useDocumentTitle("Dashboard");
  const { data: me } = useMe();
  const summary = useDashboardSummary();

  if (summary.isPending) return <PageSkeleton />;
  if (summary.isError)
    return <ErrorState error={summary.error} onRetry={() => summary.refetch()} />;
  const s = summary.data;
  const latest = s.latest_result;
  const assessed = latest?.competencies.filter((c) => c.assessed && c.percentage !== null) ?? [];

  return (
    <div className="space-y-10">
      <header className="rounded-[var(--radius-card)] bg-navy-900 px-6 py-7 text-white shadow-sm">
        <p className="text-sm font-medium text-white/75">Participant dashboard</p>
        <h1 className="mt-1 text-2xl font-semibold text-white md:text-3xl">
          Welcome, {me?.display_name}
        </h1>
        <p className="mt-2 text-white/85">Your AI-readiness assessments, results and progress.</p>
      </header>
      <DraftContentBanner provenance={s.content_provenance} />

      <section aria-labelledby="tracks-heading" className="space-y-3">
        <h2 id="tracks-heading" className="text-lg font-semibold">
          Your assessments
        </h2>
        <ul className="grid gap-4 sm:grid-cols-2">
          {s.tracks.map((t) => (
            <li key={t.track_id}>
              <TrackCard t={t} />
            </li>
          ))}
        </ul>
      </section>

      <section aria-labelledby="latest-heading" className="space-y-3">
        <h2 id="latest-heading" className="text-lg font-semibold">
          Latest result
        </h2>
        {!latest ? (
          <EmptyState title="No results yet">
            <p className="text-sm text-text-muted">
              Complete an assessment to see your competency snapshot.
            </p>
          </EmptyState>
        ) : (
          <>
            <p className="text-sm text-text-muted">
              {latest.track_name} · {formatDate(latest.submitted_at)} ·{" "}
              <span className="font-semibold text-text-primary">{latest.overall_score}/100</span> (
              {BAND_LABEL[latest.readiness_band]}) ·{" "}
              <Link
                className="text-blue-700 underline"
                to={`/attempts/${latest.attempt_id}/results`}
              >
                Full results
              </Link>
            </p>
            <ChartFigure
              caption="Competency snapshot (latest attempt)"
              chart={
                <PercentBarChart
                  data={assessed.map((c) => ({ label: c.label, value: c.percentage ?? 0 }))}
                />
              }
              table={
                <DataTable
                  caption="Competency snapshot data"
                  headers={["Competency", "Score", "Status"]}
                  rows={latest.competencies.map((c) => [
                    c.label,
                    c.percentage === null ? "Not assessed" : `${c.percentage}%`,
                    c.percentage === null
                      ? "Not assessed"
                      : c.percentage < 60
                        ? "Improvement area"
                        : "Strength",
                  ])}
                />
              }
            />
          </>
        )}
      </section>

      <section aria-labelledby="history-heading" className="space-y-3">
        <h2 id="history-heading" className="text-lg font-semibold">
          Score history
        </h2>
        {s.score_history.length === 0 ? (
          <p className="text-sm text-text-muted">You have not submitted an assessment yet.</p>
        ) : (
          <ChartFigure
            caption="Overall score by submitted attempt"
            chart={
              <ColumnChart
                max={100}
                data={s.score_history.map((h, i) => ({
                  label: `#${i + 1}`,
                  value: h.overall_score,
                }))}
              />
            }
            table={
              <DataTable
                caption="Submitted assessments"
                headers={["Attempt", "Track", "Submitted", "Score", "Versions", "Results"]}
                rows={s.score_history.map((h, i) => [
                  `#${i + 1}`,
                  h.track_name,
                  formatDate(h.submitted_at),
                  `${h.overall_score} / 100`,
                  `${h.question_bank} · ${h.scoring_policy}`,
                  <Link
                    key={h.attempt_id}
                    className="text-blue-700 underline"
                    to={`/attempts/${h.attempt_id}/results`}
                  >
                    View results{" "}
                    <span className="sr-only">
                      for attempt {i + 1}, {h.track_name}
                    </span>
                  </Link>,
                ])}
              />
            }
          />
        )}
        <p className="text-xs text-text-muted">
          Compare scores only between attempts with the same question bank and scoring policy
          versions.
        </p>
      </section>
    </div>
  );
}
