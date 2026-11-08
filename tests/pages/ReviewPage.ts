import { expect, type Page } from "@playwright/test";

export class ReviewPage {
  constructor(private readonly page: Page) {}
  readonly submitButton = () => this.page.getByRole("button", { name: "Submit assessment" });
  readonly summary = () => this.page.getByTestId("review-summary");
  readonly dialog = () => this.page.getByRole("dialog", { name: "Submit your assessment?" });

  async expectLoaded() {
    await expect(this.page.getByRole("heading", { name: "Review your answers" })).toBeVisible();
  }

  unanswered() {
    return this.page.getByRole("list", { name: "Questions" }).getByText("Not answered");
  }

  async submitAndConfirm() {
    await this.submitButton().click();
    await expect(this.dialog()).toBeVisible();
    await this.dialog().getByRole("button", { name: "Confirm submission" }).click();
  }
}
