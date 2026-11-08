import { expect, test } from "../fixtures/test";

test("TC-005 another participant cannot read or modify an attempt @regression", async ({ api, otherApi }) => {
  const attempt = await api.freshAttempt("manual_qa");
  const qid = attempt.questions[0]!.question_id;
  const base = `/attempts/${attempt.id}`;
  const responses = await Promise.all([
    otherApi.get(base),
    otherApi.put(`${base}/answers/${qid}`, { selected_option_id: "A" }),
    otherApi.get(`${base}/review`),
    otherApi.post(`${base}/submit`),
    otherApi.get(`${base}/results`),
  ]);
  for (const r of responses) {
    expect(r.status()).toBe(404);
    expect((await r.json()).code).toBe("ATTEMPT_NOT_FOUND");
  }
  const mine = await api.json<{ questions: { selected_option_id: string | null }[] }>(api.get(base));
  expect(mine.questions[0]!.selected_option_id).toBeNull();
});
