import type { ReactNode } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const BLUE = "#2563eb";
const GRID = "#e2e8f0";
const MUTED = "#475569";

/**
 * Accessible chart pattern: the SVG is decorative (aria-hidden) and every chart is paired with a
 * data table that carries the same information (DESIGN_SYSTEM.md: chart data table alternative).
 * The chart is also inert and has Recharts' keyboard layer off, so no hidden element is focusable.
 */
export function ChartFigure({
  caption,
  chart,
  table,
}: {
  caption: string;
  chart: ReactNode;
  table: ReactNode;
}) {
  return (
    <figure className="space-y-3">
      <figcaption className="font-semibold text-navy-900">{caption}</figcaption>
      <div
        aria-hidden="true"
        inert
        className="h-64 w-full rounded-[var(--radius-card)] border border-border bg-surface p-3"
      >
        {chart}
      </div>
      {table}
    </figure>
  );
}

export function PercentBarChart({ data }: { data: { label: string; value: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={data}
        layout="vertical"
        margin={{ left: 8, right: 16 }}
        accessibilityLayer={false}
      >
        <CartesianGrid stroke={GRID} horizontal={false} />
        <XAxis
          type="number"
          domain={[0, 100]}
          tickFormatter={(v) => `${v}%`}
          stroke={MUTED}
          fontSize={12}
        />
        <YAxis type="category" dataKey="label" width={170} stroke={MUTED} fontSize={12} />
        <Tooltip formatter={(v) => [`${v}%`, "Score"]} />
        <Bar dataKey="value" fill={BLUE} radius={[0, 4, 4, 0]} isAnimationActive={false} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function ColumnChart({
  data,
  max,
  unit = "",
}: {
  data: { label: string; value: number }[];
  max?: number;
  unit?: string;
}) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 8, right: 8 }} accessibilityLayer={false}>
        <CartesianGrid stroke={GRID} vertical={false} />
        <XAxis dataKey="label" stroke={MUTED} fontSize={12} interval={0} />
        <YAxis domain={[0, max ?? "auto"]} allowDecimals={false} stroke={MUTED} fontSize={12} />
        <Tooltip formatter={(v) => [`${v}${unit}`, ""]} />
        <Bar
          dataKey="value"
          fill={BLUE}
          radius={[4, 4, 0, 0]}
          maxBarSize={64}
          isAnimationActive={false}
        />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function DataTable({
  caption,
  headers,
  rows,
}: {
  caption: string;
  headers: string[];
  rows: (string | number | ReactNode)[][];
}) {
  return (
    <div className="overflow-x-auto rounded-[var(--radius-card)] border border-border bg-surface">
      <table className="w-full text-left text-sm">
        <caption className="sr-only">{caption}</caption>
        <thead className="bg-navy-900/5 text-navy-900">
          <tr>
            {headers.map((h) => (
              <th key={h} scope="col" className="px-4 py-2 font-medium">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i} className="border-t border-border">
              {r.map((cell, j) =>
                j === 0 ? (
                  <th key={j} scope="row" className="px-4 py-2 font-medium">
                    {cell}
                  </th>
                ) : (
                  <td key={j} className="px-4 py-2 tabular-nums">
                    {cell}
                  </td>
                ),
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function StatTile({
  label,
  value,
  hint,
}: {
  label: string;
  value: ReactNode;
  hint?: string;
}) {
  return (
    <div className="rounded-[var(--radius-card)] border border-border border-l-4 border-l-blue-600 bg-surface p-4 shadow-sm">
      <p className="text-sm text-text-muted">{label}</p>
      <p className="mt-1 text-2xl font-semibold text-navy-900">{value}</p>
      {hint && <p className="mt-1 text-xs text-text-muted">{hint}</p>}
    </div>
  );
}
