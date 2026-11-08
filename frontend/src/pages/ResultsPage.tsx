import { Link, useParams } from "react-router";
import { isApiError } from "@/api/errors";
import { useResults } from "@/api/queries/assessments";
import { DraftContentBanner } from "@/components/DraftContentBanner";
import { CompetencyTable, RecommendationList, ScoreCard } from "@/components/results";
import { ErrorState, PageSkeleton } from "@/components/States";
import { Button } from "@/components/ui/button";
import { formatDate, useDocumentTitle } from "@/lib/format";
import { NotFoundPage } from "./NotFoundPage";

export function ResultsPage() {
  useDocumentTitle("Results");
  const { id = "" } = useParams();
  const results = useResults(id);

  if (results.isPending) return <PageSkeleton />;
  if (results.isError) {
    if (isApiError(results.error, 404)) return <NotFoundPage />;
    if (isApiError(results.error, 409))
      return (
        <div className="space-y-4">
          <h1 className="text-2xl font-semibold">Results not available yet</h1>
          <p>Submit this assessment to see your results.</p>
          <Button asChild>
            <Link to={`/attempts/${id}/review`}>Go to review</Link>
          </Button>
        </div>
      );
    return <ErrorState error={results.error} onRetry={() => results.refetch()} />;
  }
  const r = results.data;
  const strengths = r.competencies.filter((c) => c.assessed && (c.percentage ?? 0) >= 60);
  const improvements = r.competencies.filter((c) => c.assessed && (c.percentage ?? 0) < 60);

  return (
    <div className="space-y-8">
      <DraftContentBanner provenance={r.content_provenance} />
      <header>
        <p className="text-sm text-text-muted">{r.track_name}</p>
        <h1 className="text-2xl font-semibold">Your results</h1>
      </header>

      <ScoreCard result={r} />

      <section aria-labelledby="summary-heading" className="grid gap-4 sm:grid-cols-2">
        <h2 id="summary-heading" className="sr-only">Summary</h2>
        <div>
          <h3 className="font-semibold">Strengths</h3>
          <p className="text-sm text-text-muted">
            {strengths.length ? strengths.map((c) => c.label).join(", ") : "None identified yet."}
          </p>
        </div>
        <div>
          <h3 className="font-semibold">Areas for improvement</h3>
          <p className="text-sm text-text-muted">
            {improvements.length ? improvements.map((c) => c.label).join(", ") : "None identified."}
          </p>
        </div>
      </section>

      <section aria-labelledby="competency-heading" className="space-y-3">
        <h2 id="competency-heading" className="text-lg font-semibold">Competency breakdown</h2>
        <CompetencyTable competencies={r.competencies} />
      </section>

      <section aria-labelledby="recommendations-heading" className="space-y-3">
        <h2 id="recommendations-heading" className="text-lg font-semibold">Recommendations</h2>
        <RecommendationList items={r.recommendations} />
      </section>

      <section aria-labelledby="details-heading" className="space-y-2 text-sm">
        <h2 id="details-heading" className="text-lg font-semibold">Assessment details</h2>
        <dl className="grid gap-x-6 gap-y-2 sm:grid-cols-[max-content_1fr]">
          <dt className="text-text-muted">Track</dt>
          <dd>{r.track_name}</dd>
          <dt className="text-text-muted">Submitted</dt>
          <dd>{formatDate(r.submitted_at)}</dd>
          <dt className="text-text-muted">Attempt ID</dt>
          <dd className="break-all font-mono text-xs">{r.attempt_id}</dd>
          <dt className="text-text-muted">Question bank</dt>
          <dd>{r.versions.question_bank}</dd>
          <dt className="text-text-muted">Scoring policy</dt>
          <dd>{r.versions.scoring_policy}</dd>
          <dt className="text-text-muted">Recommendation rules</dt>
          <dd>{r.versions.recommendation_rules ?? "—"}</dd>
        </dl>
        <p className="pt-2 text-text-muted">{r.disclaimer}</p>
      </section>

      <Button asChild variant="outline">
        <Link to="/">Back to dashboard</Link>
      </Button>
    </div>
  );
}
