import { readdirSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

/**
 * Expected answers are read from the seed files, never from the API (which must not expose them).
 * Keyed by prompt text, which is unique in the bank.
 */
interface SeedQuestion {
  code: string;
  competency: string;
  prompt: string;
  correct_option_id: string;
}

const dir = fileURLToPath(new URL("../../database/seed/placeholder_bank_v0/questions/", import.meta.url));
const byPrompt = new Map<string, SeedQuestion>();
for (const file of readdirSync(dir).filter((f) => f.endsWith(".json"))) {
  const data = JSON.parse(readFileSync(dir + file, "utf-8")) as { questions: SeedQuestion[] };
  for (const q of data.questions) byPrompt.set(q.prompt, q);
}

export function seedQuestion(prompt: string): SeedQuestion {
  const q = byPrompt.get(prompt);
  if (!q) throw new Error(`Prompt not found in seed bank: ${prompt}`);
  return q;
}

export const correctOptionFor = (prompt: string) => seedQuestion(prompt).correct_option_id;
export const wrongOptionFor = (prompt: string) => (correctOptionFor(prompt) === "A" ? "B" : "A");

export const TRACKS = [
  { id: "manual_qa", name: "Manual QA Engineer" },
  { id: "automation_qa", name: "Automation QA Engineer" },
  { id: "sdet", name: "SDET" },
  { id: "qa_lead", name: "QA Lead" },
] as const;

/** Mirrors DEC-02 bands for computing expectations in tests. */
export function expectedBand(score: number) {
  if (score >= 80) return "Advanced (80–100)";
  if (score >= 60) return "Proficient (60–79)";
  if (score >= 40) return "Developing (40–59)";
  return "Foundation (0–39)";
}
