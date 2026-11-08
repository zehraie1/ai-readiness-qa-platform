import { config } from "dotenv";
import { fileURLToPath } from "node:url";

config({ path: fileURLToPath(new URL("../../.env", import.meta.url)), quiet: true });

export const BASE_URL = process.env.BASE_URL ?? "http://localhost:5173";
export const API_BASE_URL = process.env.API_BASE_URL ?? "http://localhost:8000";
export const PARTICIPANT_PASSWORD = required("SEED_PARTICIPANT_PASSWORD");
export const ADMIN_PASSWORD = required("SEED_ADMIN_PASSWORD");

/** Seeded e2e participants: e2e-participant-00..07. Worker N uses N; N+4 is its "other user". */
export const MAX_WORKERS = 4;
export const participantEmail = (index: number) => `e2e-participant-${String(index).padStart(2, "0")}@example.com`;
export const ADMIN_EMAIL = "e2e-admin@example.com";

function required(name: string): string {
  const v = process.env[name];
  if (!v) throw new Error(`${name} must be set (copy .env.example to .env)`);
  return v;
}
