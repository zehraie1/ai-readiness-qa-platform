import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { result } from "@/test/fixtures";
import { CompetencyTable, RecommendationList, ScoreCard } from "./results";

describe("results components", () => {
  it("shows score, band text with range and the common/track split", () => {
    render(<ScoreCard result={result} />);
    expect(screen.getByTestId("overall-score")).toHaveTextContent("45 / 100");
    expect(screen.getByText("Developing (40–59)")).toBeInTheDocument();
    expect(screen.getByText("30 / 50")).toBeInTheDocument();
    expect(screen.getByText("15 / 50")).toBeInTheDocument();
  });

  it("renders an accessible competency table with text statuses", () => {
    render(<CompetencyTable competencies={result.competencies} />);
    const table = screen.getByRole("table", { name: "Competency breakdown" });
    const rows = within(table).getAllByRole("row");
    expect(rows).toHaveLength(4);
    expect(within(rows[1]!).getByText("Improvement area")).toBeInTheDocument();
    expect(within(rows[2]!).getByText("Strength")).toBeInTheDocument();
    expect(within(rows[3]!).getAllByText("Not assessed").length).toBeGreaterThan(0);
  });

  it("lists recommendations or explains why there are none", () => {
    const { rerender } = render(<RecommendationList items={result.recommendations} />);
    expect(screen.getByRole("heading", { name: "Build data checks" })).toBeInTheDocument();
    rerender(<RecommendationList items={[]} />);
    expect(screen.getByText(/No recommendations/)).toBeInTheDocument();
  });
});
