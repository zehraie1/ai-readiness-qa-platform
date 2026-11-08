import { expect, type Page } from "@playwright/test";

export class LoginPage {
  constructor(private readonly page: Page) {}
  readonly email = () => this.page.getByLabel("Email");
  readonly password = () => this.page.getByLabel("Password");
  readonly submit = () => this.page.getByRole("button", { name: "Sign in" });
  readonly error = () => this.page.getByRole("alert");

  async goto(next?: string) {
    await this.page.goto(next ? `/login?next=${encodeURIComponent(next)}` : "/login");
    await expect(this.page.getByRole("heading", { name: "Sign in" })).toBeVisible();
  }

  async signIn(email: string, password: string) {
    await this.email().fill(email);
    await this.password().fill(password);
    await this.submit().click();
  }
}
