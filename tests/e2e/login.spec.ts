import { expect, test } from "../fixtures/test";
import { ADMIN_EMAIL, ADMIN_PASSWORD } from "../fixtures/env";
import { LoginPage } from "../pages/LoginPage";

test.describe("sign-in @smoke", () => {
  test.use({ storageState: { cookies: [], origins: [] } });

  test("invalid credentials show a generic error", async ({ page, account }) => {
    const login = new LoginPage(page);
    await login.goto();
    await login.signIn(account.email, "definitely-wrong");
    await expect(login.error()).toHaveText("Email or password is incorrect.");
  });

  test("protected page redirects to sign-in and back", async ({ page, account }) => {
    await page.goto("/assessments/tracks");
    await expect(page).toHaveURL(/\/login\?next=/);
    await new LoginPage(page).signIn(account.email, account.password);
    await expect(page).toHaveURL(/\/assessments\/tracks$/);
    await expect(page.getByRole("heading", { name: "Choose an assessment track" })).toBeVisible();
  });

  test("administrator lands on admin and is denied participant pages", async ({ page }) => {
    const login = new LoginPage(page);
    await login.goto();
    await login.signIn(ADMIN_EMAIL, ADMIN_PASSWORD);
    await expect(page.getByRole("heading", { name: "Administration" })).toBeVisible();
    await page.goto("/assessments/tracks");
    await expect(page.getByRole("heading", { name: "You do not have access to this page" })).toBeVisible();
  });

  // Uses its own session: signing out revokes the session server-side, so it must not be the
  // worker's shared storage-state session.
  test("participant can sign out", async ({ page, account }) => {
    const login = new LoginPage(page);
    await login.goto();
    await login.signIn(account.email, account.password);
    await expect(page.getByRole("heading", { name: /Welcome/ })).toBeVisible();
    await page.getByRole("button", { name: "Sign out" }).click();
    await expect(page.getByRole("heading", { name: "Sign in" })).toBeVisible();
    await page.goto("/");
    await expect(page).toHaveURL(/\/login/);
  });
});
