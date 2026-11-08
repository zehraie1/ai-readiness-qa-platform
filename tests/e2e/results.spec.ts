import { expect, test } from "../fixtures/test";
import { expectedBand, seedQuestion } from "../data/bank";
import { ResultsPage } from "../pages/ResultsPage";

test("results show score, band, competencies and recommendations for a known answer pattern @regression", async ({
  page,
  api,
}) => {
  const attempt = await api.freshAttempt("manual_qa");
  const correct = new Set([1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14]); // 11 correct => 55
  await api.answerAll(attempt, correct);
  await api.json(api.post(`/attempts/${attempt.id}/submit`));

  // Expected competency figures computed independently from the seed bank.
  const tallies = new Map<string, { correct: number; total: number }>();
  for (const q of attempt.questions) {
    const t = tallies.get(seedQuestion(q.prompt).competency) ?? { correct: 0, total: 0 };
    t.total += 1;
    t.correct += correct.has(q.position) ? 1 : 0;
    tallies.set(seedQuestion(q.prompt).competency, t);
  }

  await page.goto(`/attempts/${attempt.id}/results`);
  const results = new ResultsPage(page);
  await results.expectLoaded();
  await expect(results.score()).toHaveText("55 / 100");
  await expect(page.getByText(expectedBand(55))).toBeVisible();
  await expect(page.getByText("35 / 50")).toBeVisible();
  await expect(page.getByText("20 / 50")).toBeVisible();
  await expect(results.draftBanner()).toBeVisible();

  const result = await api.json<{ competencies: { code: string; label: string; correct: number; total: number; percentage: number | null }[]; recommendations: unknown[] }>(
    api.get(`/attempts/${attempt.id}/results`),
  );
  for (const c of result.competencies) {
    const t = tallies.get(c.code);
    const row = results.competencyRow(c.label);
    if (!t) {
      await expect(row).toContainText("Not assessed");
      continue;
    }
    expect([c.correct, c.total]).toEqual([t.correct, t.total]);
    await expect(row).toContainText(`${t.correct} / ${t.total}`);
    await expect(row).toContainText(c.percentage! < 60 ? "Improvement area" : "Strength");
  }
  const below = result.competencies.filter((c) => c.percentage !== null && c.percentage < 60).length;
  expect(result.recommendations).toHaveLength(below);
  await expect(results.recommendations()).toHaveCount(below);
});
