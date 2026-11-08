import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "../fixtures/test";

const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];

async function expectNoViolations(page: import("@playwright/test").Page) {
  const { violations } = await new AxeBuilder({ page }).withTags(TAGS).analyze();
  expect(violations.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(" ")).join(", ")}`)).toEqual([]);
}

test.describe("TC-013 automated accessibility checks (manual review still required) @a11y", () => {
  test("login page", async ({ browser }) => {
    const ctx = await browser.newContext({ storageState: { cookies: [], origins: [] } });
    const page = await ctx.newPage();
    await page.goto("/login");
    await expect(page.getByRole("heading", { name: "Sign in" })).toBeVisible();
    await expectNoViolations(page);
    await ctx.close();
  });

  test("dashboard, tracks, question, review and results pages", async ({ page, api }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: /Welcome/ })).toBeVisible();
    await expectNoViolations(page);

    await page.goto("/assessments/tracks");
    await expect(page.getByRole("heading", { name: "Choose an assessment track" })).toBeVisible();
    await expectNoViolations(page);

    const a = await api.freshAttempt("automation_qa");
    await page.goto(`/attempts/${a.id}/questions/1`);
    await expect(page.getByRole("heading", { name: "Question 1 of 20" })).toBeVisible();
    await expectNoViolations(page);

    await page.goto(`/attempts/${a.id}/review`);
    await expect(page.getByRole("heading", { name: "Review your answers" })).toBeVisible();
    await expectNoViolations(page);

    await api.answerAll(a, new Set([1, 2, 3]));
    await api.json(api.post(`/attempts/${a.id}/submit`));
    await page.goto(`/attempts/${a.id}/results`);
    await expect(page.getByRole("heading", { name: "Your results" })).toBeVisible();
    await expectNoViolations(page);
  });
});
