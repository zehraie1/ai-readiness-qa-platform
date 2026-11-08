import { expect, type Page } from "@playwright/test";

export class QuestionPage {
  constructor(private readonly page: Page) {}
  readonly heading = () => this.page.getByRole("heading", { level: 1 });
  readonly options = () => this.page.getByRole("radio");
  readonly saveStatus = () => this.page.getByRole("status").filter({ hasText: /saved|Saving|could not/i });
  readonly stepper = () => this.page.getByRole("navigation", { name: "Question navigator" });

  option(id: string) {
    return this.page.getByRole("radio", { name: new RegExp(`^${id}\\.`) });
  }

  async prompt(): Promise<string> {
    return (await this.page.getByRole("radiogroup").getAttribute("aria-labelledby").then((id) =>
      this.page.locator(`[id="${id}"]`).innerText(),
    )).trim();
  }

  async expectAt(position: number, total = 20) {
    await expect(this.heading()).toHaveText(`Question ${position} of ${total}`);
  }

  async expectAnswered(count: number, total = 20) {
    await expect(this.page.getByText(`${count} of ${total} answered`)).toBeVisible();
  }

  async choose(id: string) {
    await this.option(id).click();
    await expect(this.option(id)).toBeChecked();
    await expect(this.page.getByText("Answer saved")).toBeVisible();
  }

  next = () => this.page.getByRole("link", { name: /^Next/ }).click();
  previous = () => this.page.getByRole("link", { name: /^Previous/ }).click();
  review = () => this.page.getByRole("link", { name: /Review answers|Finish and review/ }).first().click();
}
