import { expect, type Page } from "@playwright/test";

export class TracksPage {
  constructor(private readonly page: Page) {}

  async goto() {
    await this.page.goto("/assessments/tracks");
    await expect(this.page.getByRole("heading", { name: "Choose an assessment track" })).toBeVisible();
  }

  startButton(trackName: string) {
    return this.page.getByRole("button", { name: `Start ${trackName}`, exact: true });
  }

  dialog() {
    return this.page.getByRole("dialog");
  }

  async start(trackName: string) {
    await this.startButton(trackName).click();
    await expect(this.dialog().getByRole("heading", { name: `Start ${trackName}` })).toBeVisible();
    await this.dialog().getByRole("button", { name: "Begin assessment" }).click();
  }
}
