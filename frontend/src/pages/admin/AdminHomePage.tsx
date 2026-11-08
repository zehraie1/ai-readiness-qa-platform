import { AlertTriangle } from "lucide-react";
import { useAdminDashboardSummary } from "@/api/queries/assessments";
import { ChartFigure, ColumnChart, DataTable, StatTile } from "@/components/charts";
import { DraftContentBanner } from "@/components/DraftContentBanner";
import { ErrorState, PageSkeleton } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { formatDate, useDocumentTitle } from "@/lib/format";

export function AdminHomePage() {
  useDocumentTitle("Administration");
  const summary = useAdminDashboardSummary();
  if (summary.isPending) return <PageSkeleton />;
  if (summary.isError) return <ErrorState error={summary.error} onRetry={() => summary.refetch()} />;
  const s = summary.data;
  const submittedTotal = s.tracks.reduce((n, t) => n + t.attempts_submitted, 0);

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-2xl font-semibold">Administration</h1>
        <p className="mt-1 text-text-muted">
          Aggregate overview. Individual participants are not ranked or listed. Content management arrives in
          a later phase.
        </p>
      </header>
      <DraftContentBanner provenance={s.published_bank?.content_provenance} />

      {s.warnings.length > 0 && (
        <section aria-labelledby="warnings-heading">
          <h2 id="warnings-heading" className="sr-only">Data quality warnings</h2>
          <Alert tone="warning">
            <AlertTriangle aria-hidden="true" />
            <ul className="list-disc space-y-1 pl-4">
              {s.warnings.map((w) => (
                <li key={w}>{w}</li>
              ))}
            </ul>
          </Alert>
        </section>
      )}

      <section aria-labelledby="overview-heading" className="space-y-3">
        <h2 id="overview-heading" className="text-lg font-semibold">Overview</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatTile
            label="Published question bank"
            value={s.published_bank?.version_label ?? "None"}
            hint={s.published_bank ? `Published ${formatDate(s.published_bank.published_at)}` : undefined}
          />
          <StatTile label="Participants" value={s.participants_total} />
          <StatTile label="Participants with results" value={s.participants_with_results} />
          <StatTile label="Submitted assessments" value={submittedTotal} />
        </div>
      </section>

      <section aria-labelledby="tracks-heading" className="space-y-3">
        <h2 id="tracks-heading" className="text-lg font-semibold">Completion by track</h2>
        <DataTable
          caption="Assessment completion by track"
          headers={["Track", "Started", "Submitted", "Average score"]}
          rows={s.tracks.map((t) => [
            t.track_name,
            t.attempts_started,
            t.attempts_submitted,
            t.average_score === null ? "—" : `${t.average_score} / 100`,
          ])}
        />
      </section>

      <section aria-labelledby="bands-heading" className="space-y-3">
        <h2 id="bands-heading" className="text-lg font-semibold">Readiness level distribution</h2>
        <ChartFigure
          caption="Submitted assessments by readiness level"
          chart={<ColumnChart data={s.band_distribution.map((b) => ({ label: b.label, value: b.count }))} />}
          table={
            <DataTable
              caption="Readiness level distribution data"
              headers={["Readiness level", "Assessments"]}
              rows={s.band_distribution.map((b) => [b.label, b.count])}
            />
          }
        />
      </section>

      <section aria-labelledby="content-heading" className="grid gap-6 lg:grid-cols-2">
        <h2 id="content-heading" className="sr-only">Question bank coverage</h2>
        <div className="space-y-3">
          <h3 className="font-semibold">Questions by scope</h3>
          <DataTable
            caption="Questions by scope"
            headers={["Scope", "Questions"]}
            rows={s.questions_by_scope.map((q) => [q.label, q.count])}
          />
        </div>
        <div className="space-y-3">
          <h3 className="font-semibold">Questions by competency</h3>
          <DataTable
            caption="Questions by competency"
            headers={["Competency", "Questions"]}
            rows={s.questions_by_competency.map((q) => [q.label, q.count])}
          />
        </div>
      </section>
    </div>
  );
}
