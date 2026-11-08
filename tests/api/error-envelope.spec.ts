import { expect, test } from "../fixtures/test";

const KEYS = ["code", "details", "message", "request_id"];

test.describe("TC-015 consistent error envelope @regression", () => {
  test("401, 403, 404, 409 and 422 share the envelope and echo the request id", async ({ api, anonApi }) => {
    const a = await api.freshAttempt("sdet");
    const cases = [
      { res: await anonApi.get("/me"), status: 401, code: "UNAUTHENTICATED" },
      { res: await api.get("/admin/competencies"), status: 403, code: "FORBIDDEN" },
      { res: await api.get("/attempts/00000000-0000-0000-0000-000000000000"), status: 404, code: "ATTEMPT_NOT_FOUND" },
      { res: await api.get(`/attempts/${a.id}/results`), status: 409, code: "RESULTS_NOT_AVAILABLE" },
      { res: await api.post("/attempts", {}), status: 422, code: "VALIDATION_ERROR" },
    ];
    for (const c of cases) {
      expect(c.res.status()).toBe(c.status);
      const body = await c.res.json();
      expect(Object.keys(body).sort()).toEqual(KEYS);
      expect(body.code).toBe(c.code);
      expect(body.request_id).toBe(c.res.headers()["x-request-id"]);
    }
  });

  test("requests from a foreign origin are rejected", async ({ api }) => {
    const r = await api.ctx.post("/api/v1/attempts", {
      data: { track_id: "sdet" },
      headers: { Origin: "https://evil.example" },
    });
    expect(r.status()).toBe(403);
    expect((await r.json()).code).toBe("CSRF_REJECTED");
  });
});
