import { CheckCircle2, CircleMinus, TrendingUp } from "lucide-react";
import type { CompetencyResult, Recommendation, Result } from "@/api/types";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

const THRESHOLD = 60; // DEC-03 approved trigger, mirrored for labelling only; server decides recommendations.

export function ReadinessBadge({ band }: { band: Result["readiness_band"] }) {
  const tone =
    band.code === "advanced" || band.code === "proficient"
      ? "success"
      : band.code === "developing"
        ? "info"
        : "warning";
  return (
    <Badge tone={tone} className="text-sm">
      {band.label} ({band.min}–{band.max})
    </Badge>
  );
}

const BAND_ACCENT: Record<string, string> = {
  advanced: "border-l-success",
  proficient: "border-l-success",
  developing: "border-l-blue-600",
  foundation: "border-l-warning",
};

export function ScoreCard({ result }: { result: Result }) {
  return (
    <Card
      className={`grid gap-6 border-l-8 sm:grid-cols-[auto_1fr] sm:items-center ${BAND_ACCENT[result.readiness_band.code] ?? "border-l-blue-600"}`}
    >
      <div>
        <p className="text-sm text-text-muted">Overall score</p>
        <p className="text-5xl font-bold tracking-tight text-navy-900" data-testid="overall-score">
          {result.overall_score}
          <span className="text-2xl font-medium text-text-muted"> / {result.max_score}</span>
        </p>
        <p className="mt-1 text-sm text-text-muted">
          {result.correct_count} of {result.total_questions} correct
        </p>
      </div>
      <dl className="grid grid-cols-2 gap-x-6 gap-y-3 text-sm sm:justify-self-end">
        <div className="col-span-2">
          <dt className="text-text-muted">Readiness level</dt>
          <dd className="mt-1">
            <ReadinessBadge band={result.readiness_band} />
          </dd>
        </div>
        <div>
          <dt className="text-text-muted">Common questions</dt>
          <dd className="font-semibold">{result.common_score} / 50</dd>
        </div>
        <div>
          <dt className="text-text-muted">Track questions</dt>
          <dd className="font-semibold">{result.role_specific_score} / 50</dd>
        </div>
      </dl>
    </Card>
  );
}

function statusOf(c: CompetencyResult) {
  if (!c.assessed || c.percentage == null)
    return { label: "Not assessed", icon: CircleMinus, tone: "neutral" as const };
  if (c.percentage < THRESHOLD)
    return { label: "Improvement area", icon: TrendingUp, tone: "warning" as const };
  return { label: "Strength", icon: CheckCircle2, tone: "success" as const };
}

/** The table is the primary, accessible representation; the bar is decorative. */
export function CompetencyTable({ competencies }: { competencies: CompetencyResult[] }) {
  return (
    <div className="overflow-x-auto rounded-[var(--radius-card)] border border-border bg-surface">
      <table className="w-full text-left text-sm">
        <caption className="sr-only">Competency breakdown</caption>
        <thead className="bg-navy-900/5 text-navy-900">
          <tr>
            <th scope="col" className="px-4 py-3 font-medium">
              Competency
            </th>
            <th scope="col" className="px-4 py-3 font-medium">
              Correct
            </th>
            <th scope="col" className="px-4 py-3 font-medium">
              Score
            </th>
            <th scope="col" className="px-4 py-3 font-medium">
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          {competencies.map((c) => {
            const s = statusOf(c);
            return (
              <tr key={c.code} className="border-t border-border">
                <th scope="row" className="px-4 py-3 font-medium">
                  {c.label}
                </th>
                <td className="px-4 py-3">{c.assessed ? `${c.correct} / ${c.total}` : "—"}</td>
                <td className="px-4 py-3">
                  {c.percentage == null ? (
                    "Not assessed"
                  ) : (
                    <div className="flex items-center gap-3">
                      <span className="w-10 tabular-nums">{c.percentage}%</span>
                      <div
                        aria-hidden="true"
                        className="hidden h-2 w-24 rounded-full bg-border sm:block"
                      >
                        <div
                          className="h-full rounded-full bg-blue-600"
                          style={{ width: `${c.percentage}%` }}
                        />
                      </div>
                    </div>
                  )}
                </td>
                <td className="px-4 py-3">
                  <Badge tone={s.tone}>
                    <s.icon aria-hidden="true" /> {s.label}
                  </Badge>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export function RecommendationList({ items }: { items: Recommendation[] }) {
  if (items.length === 0) {
    return (
      <p className="text-sm text-text-muted">
        No recommendations: every assessed competency is at or above {THRESHOLD}%.
      </p>
    );
  }
  return (
    <ol className="space-y-3">
      {items.map((r) => (
        <li key={r.competency_code}>
          <Card className="p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-text-muted">
              {r.competency_label}
            </p>
            <h3 className="mt-1 font-semibold">{r.title}</h3>
            <p className="mt-1 text-sm text-text-muted">{r.body}</p>
          </Card>
        </li>
      ))}
    </ol>
  );
}
