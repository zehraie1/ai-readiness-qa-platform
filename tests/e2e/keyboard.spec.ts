import { expect, test } from "../fixtures/test";
import { QuestionPage } from "../pages/QuestionPage";
import { ReviewPage } from "../pages/ReviewPage";

test.describe("TC-012 keyboard and responsive (partial) @regression", () => {
  test("options can be chosen with arrow keys and the confirm dialog traps and returns focus", async ({ page, api }) => {
    const a = await api.freshAttempt("qa_lead");
    await page.goto(`/attempts/${a.id}/questions/1`);
    const q = new QuestionPage(page);
    await q.expectAt(1);

    await q.option("A").focus();
    await page.keyboard.press("Space");
    await expect(q.option("A")).toBeChecked();
    // Radix moves focus on a timer and selects only while the arrow key is still held (as with a
    // real keypress). keyboard.press() releases instantly, so hold the key like a person would.
    await page.keyboard.down("ArrowDown");
    await expect(q.option("B")).toBeChecked();
    await page.keyboard.up("ArrowDown");
    await expect(q.option("B")).toBeFocused();
    await expect(page.getByText("Answer saved")).toBeVisible();

    // Complete via API so the submit button is enabled, then test the dialog with the keyboard.
    await api.answerAll(a);
    await page.goto(`/attempts/${a.id}/review`);
    const review = new ReviewPage(page);
    await review.submitButton().focus();
    await page.keyboard.press("Enter");
    await expect(review.dialog()).toBeVisible();
    for (let i = 0; i < 4; i++) {
      await page.keyboard.press("Tab");
      const inside = await review.dialog().evaluate((d) => d.contains(document.activeElement));
      expect(inside).toBe(true);
    }
    await page.keyboard.press("Escape");
    await expect(review.dialog()).toBeHidden();
    await expect(review.submitButton()).toBeFocused();
  });

  test("question page works at 375px with navigation menu", async ({ page, api }) => {
    await page.setViewportSize({ width: 375, height: 800 });
    const a = await api.freshAttempt("qa_lead");
    await page.goto(`/attempts/${a.id}/questions/2`);
    const q = new QuestionPage(page);
    await q.expectAt(2);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    expect(overflow).toBe(false);
    const menu = page.getByRole("button", { name: "Open navigation" });
    await menu.click();
    await expect(page.getByRole("navigation", { name: "Primary" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Close navigation" })).toHaveAttribute("aria-expanded", "true");
  });
});
