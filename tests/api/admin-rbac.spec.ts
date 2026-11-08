import { expect, test } from "../fixtures/test";

test.describe("TC-006 role enforcement @smoke", () => {
  test("participants are rejected from admin endpoints", async ({ api }) => {
    const r = await api.get("/admin/competencies");
    expect(r.status()).toBe(403);
    expect((await r.json()).code).toBe("FORBIDDEN");
  });

  test("administrators can read admin endpoints but cannot take assessments", async ({ adminApi }) => {
    expect((await adminApi.get("/admin/competencies")).status()).toBe(200);
    expect((await adminApi.post("/attempts", { track_id: "sdet" })).status()).toBe(403);
  });
});
