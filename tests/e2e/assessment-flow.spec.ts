import { expect, test } from "../fixtures/test";
import { correctOptionFor } from "../data/bank";
import { QuestionPage } from "../pages/QuestionPage";
import { ResultsPage } from "../pages/ResultsPage";
import { ReviewPage } from "../pages/ReviewPage";
import { TracksPage } from "../pages/TracksPage";

test("TC-003 progress, navigation, save and resume preserve answers @smoke", async ({ page, api }) => {
  await api.freshAttempt("sdet"); // clean state: no partially answered SDET attempt
  const tracks = new TracksPage(page);
  const q = new QuestionPage(page);

  await tracks.goto();
  await tracks.start("SDET");
  await q.expectAt(1);
  await q.expectAnswered(0);

  // Answer Q1-Q5 correctly, moving forward with Next.
  for (let pos = 1; pos <= 5; pos++) {
    await q.expectAt(pos);
    await q.choose(correctOptionFor(await q.prompt()));
    await q.expectAnswered(pos);
    await q.next();
  }
  await q.expectAt(6);

  // Previous keeps earlier selections.
  await q.previous();
  await q.expectAt(5);
  await expect(page.getByRole("radio", { checked: true })).toHaveCount(1);

  // Reload: server-side persistence survives.
  await page.getByRole("link", { name: "Question 3, answered" }).click();
  await q.expectAt(3);
  await page.reload();
  await q.expectAt(3);
  await expect(page.getByRole("radio", { checked: true })).toHaveCount(1);
  await q.expectAnswered(5);

  // Resume from the dashboard lands on the first unanswered question.
  await page.goto("/");
  await page.getByRole("link", { name: "Resume SDET assessment" }).click();
  await q.expectAt(6);

  // Review shows 15 unanswered and blocks submission.
  await q.review();
  const review = new ReviewPage(page);
  await review.expectLoaded();
  await expect(review.summary()).toHaveText("5 of 20 answered");
  await expect(review.unanswered()).toHaveCount(15);
  await expect(review.submitButton()).toBeDisabled();

  // Answer the rest through the UI, then submit.
  await page.getByRole("link", { name: "Question 6", exact: true }).click();
  for (let pos = 6; pos <= 20; pos++) {
    await q.expectAt(pos);
    await q.choose(correctOptionFor(await q.prompt()));
    if (pos < 20) await q.next();
  }
  await q.review();
  await expect(review.summary()).toHaveText("20 of 20 answered");
  await expect(review.submitButton()).toBeEnabled();
  await review.submitAndConfirm();

  const results = new ResultsPage(page);
  await results.expectLoaded();
  await expect(results.score()).toHaveText("100 / 100");
});
