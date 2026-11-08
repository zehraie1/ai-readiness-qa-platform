import { test as base, expect } from "@playwright/test";
import { mkdirSync } from "node:fs";
import { ApiClient } from "./api-client";
import { ADMIN_EMAIL, ADMIN_PASSWORD, MAX_WORKERS, PARTICIPANT_PASSWORD, participantEmail } from "./env";

interface TestFixtures {
  api: ApiClient;
  otherApi: ApiClient;
  adminApi: ApiClient;
  anonApi: ApiClient;
}
interface WorkerFixtures {
  account: { email: string; password: string };
  authFile: string;
}

/**
 * Worker isolation: parallelIndex N uses seeded participant N, so concurrent workers never share
 * a user. UI tests start already signed in via a saved storage state.
 */
export const test = base.extend<TestFixtures, WorkerFixtures>({
  account: [
    async ({}, use, info) => {
      if (info.parallelIndex >= MAX_WORKERS) throw new Error("More workers than seeded e2e users");
      await use({ email: participantEmail(info.parallelIndex), password: PARTICIPANT_PASSWORD });
    },
    { scope: "worker" },
  ],
  authFile: [
    async ({ account }, use, info) => {
      mkdirSync("tests/.auth", { recursive: true });
      const file = `tests/.auth/participant-${info.parallelIndex}.json`;
      const client = await ApiClient.login(account.email, account.password);
      await client.ctx.storageState({ path: file });
      await client.dispose();
      await use(file);
    },
    { scope: "worker" },
  ],
  storageState: async ({ authFile }, use) => use(authFile),
  api: async ({ account }, use) => {
    const client = await ApiClient.login(account.email, account.password);
    await use(client);
    await client.dispose();
  },
  otherApi: async ({}, use, info) => {
    const client = await ApiClient.login(participantEmail(info.parallelIndex + MAX_WORKERS), PARTICIPANT_PASSWORD);
    await use(client);
    await client.dispose();
  },
  adminApi: async ({}, use) => {
    const client = await ApiClient.login(ADMIN_EMAIL, ADMIN_PASSWORD);
    await use(client);
    await client.dispose();
  },
  anonApi: async ({}, use) => {
    const client = await ApiClient.anonymous();
    await use(client);
    await client.dispose();
  },
});

export { expect };
