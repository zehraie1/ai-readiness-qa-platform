import { expect, test } from "../fixtures/test";

test("TC-008 concurrent submissions create exactly one result @regression", async ({ api }) => {
  const a = await api.freshAttempt("qa_lead");
  await api.answerAll(a);
  const responses = await Promise.all(Array.from({ length: 3 }, () => api.post(`/attempts/${a.id}/submit`)));
  expect(responses.map((r) => r.status())).toEqual([200, 200, 200]);
  const bodies = await Promise.all(responses.map((r) => r.text()));
  expect(new Set(bodies).size).toBe(1);

  const history = await api.json<{ items: { id: string; status: string }[] }>(
    api.get("/attempts?status=submitted&limit=50"),
  );
  expect(history.items.filter((i) => i.id === a.id)).toHaveLength(1);
});
