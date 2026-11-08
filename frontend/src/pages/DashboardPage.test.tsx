import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, within } from "@testing-library/react";
import { createMemoryRouter, RouterProvider } from "react-router";
import { describe, expect, it, vi } from "vitest";
import type { ParticipantSummary } from "@/api/types";

const summary: ParticipantSummary = {
  content_provenance: "placeholder_unverified",
  tracks: [
    {
      track_id: "manual_qa",
      track_name: "Manual QA Engineer",
      status: "not_started",
      in_progress_attempt_id: null,
      resume_position: null,
      answered_count: 0,
      attempts_completed: 0,
      latest_score: null,
      best_score: null,
      latest_band: null,
      latest_attempt_id: null,
    },
    {
      track_id: "sdet",
      track_name: "SDET",
      status: "in_progress",
      in_progress_attempt_id: "att-2",
      resume_position: 6,
      answered_count: 5,
      attempts_completed: 1,
      latest_score: 45,
      best_score: 45,
      latest_band: "developing",
      latest_attempt_id: "att-1",
    },
  ],
  latest_result: {
    attempt_id: "att-1",
    track_name: "SDET",
    submitted_at: "2026-11-08T10:00:00Z",
    overall_score: 45,
    readiness_band: "developing",
    competencies: [
      { code: "A", label: "Data quality and bias", percentage: 25, assessed: true },
      { code: "B", label: "Quality leadership", percentage: null, assessed: false },
    ],
  },
  score_history: [
    {
      attempt_id: "att-1",
      track_id: "sdet",
      track_name: "SDET",
      submitted_at: "2026-11-08T10:00:00Z",
      overall_score: 45,
      question_bank: "placeholder-v0",
      scoring_policy: "v1-simple",
    },
  ],
};

vi.mock("@/api/client", () => ({
  api: {
    GET: async (path: string) => ({
      data:
        path === "/api/v1/me"
          ? {
              id: "u",
              email: "p@example.com",
              display_name: "Pat",
              role: "participant",
              permissions: [],
            }
          : summary,
      response: new Response(null, { status: 200 }),
    }),
  },
}));

const { DashboardPage } = await import("./DashboardPage");

describe("DashboardPage", () => {
  it("shows track statuses, resume link, and table alternatives to charts", async () => {
    const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const router = createMemoryRouter([{ path: "/", element: <DashboardPage /> }]);
    render(
      <QueryClientProvider client={qc}>
        <RouterProvider router={router} />
      </QueryClientProvider>,
    );
    await screen.findByText("Your assessments", {}, { timeout: 3000 });
    expect(screen.getByRole("link", { name: /Resume SDET assessment/ })).toHaveAttribute(
      "href",
      "/attempts/att-2/questions/6",
    );
    expect(screen.getByText("Not started")).toBeInTheDocument();
    const snapshot = screen.getByRole("table", { name: "Competency snapshot data" });
    expect(
      within(snapshot).getByRole("row", { name: /Data quality and bias 25% Improvement area/ }),
    ).toBeInTheDocument();
    expect(
      within(snapshot).getByRole("row", { name: /Quality leadership Not assessed/ }),
    ).toBeInTheDocument();
    expect(screen.getByRole("table", { name: "Submitted assessments" })).toHaveTextContent(
      "45 / 100",
    );
    expect(screen.getByRole("note", { name: "Draft content notice" })).toBeInTheDocument();
  });
});
