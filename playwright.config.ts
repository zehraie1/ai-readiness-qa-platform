import { defineConfig, devices } from "@playwright/test";
import { BASE_URL, API_BASE_URL, MAX_WORKERS } from "./tests/fixtures/env";

/**
 * Prerequisites: database up, migrated and seeded with `--profile test` (see README / `make test-e2e`).
 * Each parallel worker uses its own seeded participant account (tests/fixtures/env.ts).
 */
export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: MAX_WORKERS,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: BASE_URL,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    extraHTTPHeaders: { Origin: BASE_URL },
  },
  projects: [
    { name: "setup", testMatch: /global\.setup\.ts/ },
    {
      name: "api",
      testDir: "./tests/api",
      dependencies: ["setup"],
      use: { baseURL: API_BASE_URL },
    },
    {
      name: "chromium-e2e",
      testDir: "./tests/e2e",
      dependencies: ["setup"],
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: [
    {
      command: "cd backend && .venv/bin/uvicorn app.main:app --port 8000",
      url: `${API_BASE_URL}/health`,
      reuseExistingServer: !process.env.CI,
      timeout: 60_000,
    },
    {
      command: "cd frontend && npx vite --port 5173",
      url: `${BASE_URL}/login`,
      reuseExistingServer: !process.env.CI,
      timeout: 60_000,
    },
  ],
});
