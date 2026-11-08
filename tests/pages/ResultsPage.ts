import { expect, type Page } from "@playwright/test";

export class ResultsPage {
  constructor(private readonly page: Page) {}
  readonly score = () => this.page.getByTestId("overall-score");
  readonly competencyTable = () => this.page.getByRole("table", { name: "Competency breakdown" });
  readonly recommendations = () =>
    this.page.getByRole("region", { name: "Recommendations" }).getByRole("listitem");
  readonly draftBanner = () => this.page.getByRole("note", { name: "Draft content notice" });

  async expectLoaded() {
    await expect(this.page.getByRole("heading", { name: "Your results" })).toBeVisible();
  }

  competencyRow(label: string) {
    return this.competencyTable().getByRole("row", { name: new RegExp(label) });
  }
}
