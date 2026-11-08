import { expect, test } from "../fixtures/test";
import { TRACKS } from "../data/bank";

test.describe("TC-001 assessment tracks @smoke", () => {
  test("returns the four tracks to an authenticated participant", async ({ api }) => {
    const tracks = await api.json<{ id: string; name: string; question_count: number }[]>(api.get("/assessment-tracks"));
    expect(tracks.map((t) => [t.id, t.name])).toEqual(TRACKS.map((t) => [t.id, t.name]));
    expect(tracks.every((t) => t.question_count === 20)).toBe(true);
  });

  test("is protected from anonymous access", async ({ anonApi }) => {
    const res = await anonApi.get("/assessment-tracks");
    expect(res.status()).toBe(401);
    expect((await res.json()).code).toBe("UNAUTHENTICATED");
  });
});
