import { expect, test as setup } from "@playwright/test";
import { API_BASE_URL } from "./fixtures/env";
import { ApiClient } from "./fixtures/api-client";
import { ADMIN_EMAIL, ADMIN_PASSWORD, MAX_WORKERS, PARTICIPANT_PASSWORD, participantEmail } from "./fixtures/env";

setup("environment is ready and e2e accounts are seeded", async ({ request }) => {
  const ready = await request.get(`${API_BASE_URL}/ready`);
  expect(ready.status(), "API /ready — is the database up and migrated?").toBe(200);
  for (let i = 0; i < MAX_WORKERS * 2; i++) {
    const c = await ApiClient.login(participantEmail(i), PARTICIPANT_PASSWORD);
    await c.dispose();
  }
  const admin = await ApiClient.login(ADMIN_EMAIL, ADMIN_PASSWORD);
  await admin.dispose();
});
