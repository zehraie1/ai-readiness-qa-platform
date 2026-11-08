import { expect, test } from "../fixtures/test";

const FORBIDDEN = ["correct_option_id", "explanation", "evidence_reference", "is_correct"];

function forbiddenKeys(value: unknown): string[] {
  if (Array.isArray(value)) return value.flatMap(forbiddenKeys);
  if (value && typeof value === "object") {
    return Object.entries(value).flatMap(([k, v]) => [...(FORBIDDEN.includes(k) ? [k] : []), ...forbiddenKeys(v)]);
  }
  return [];
}

test("TC-004 no answer keys in participant responses before submission @smoke", async ({ api }) => {
  const attempt = await api.freshAttempt("sdet");
  await api.answer(attempt.id, attempt.questions[0]!.question_id, "A");
  const responses = await Promise.all([
    api.get(`/attempts/${attempt.id}`),
    api.get(`/attempts/${attempt.id}/review`),
    api.get("/attempts"),
    api.get("/assessment-tracks"),
  ]);
  for (const r of [attempt, ...(await Promise.all(responses.map((x) => x.json())))]) {
    expect(forbiddenKeys(r)).toEqual([]);
  }
});
