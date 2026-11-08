import { expect, test } from "../fixtures/test";

test.describe("TC-007 answer validation @regression", () => {
  test("rejects an option that is not A-D", async ({ api }) => {
    const a = await api.freshAttempt("automation_qa");
    const r = await api.answer(a.id, a.questions[0]!.question_id, "E");
    expect(r.status()).toBe(422);
    expect((await r.json()).code).toBe("INVALID_OPTION");
  });

  test("rejects stale answers after submission", async ({ api }) => {
    const a = await api.freshAttempt("automation_qa");
    await api.answerAll(a);
    await api.json(api.post(`/attempts/${a.id}/submit`));
    const r = await api.answer(a.id, a.questions[5]!.question_id, "B");
    expect(r.status()).toBe(409);
    expect((await r.json()).code).toBe("ATTEMPT_CLOSED");
  });

  test("rejects incomplete submission with the unanswered positions", async ({ api }) => {
    const a = await api.freshAttempt("automation_qa");
    await api.answerAll({ ...a, questions: a.questions.slice(0, 19) });
    const r = await api.post(`/attempts/${a.id}/submit`);
    expect(r.status()).toBe(409);
    const body = await r.json();
    expect(body.code).toBe("ATTEMPT_INCOMPLETE");
    expect(body.details.unanswered_positions).toEqual([20]);
  });
});
