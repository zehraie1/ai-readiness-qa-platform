import { expect, test } from "../fixtures/test";
import { seedQuestion, TRACKS } from "../data/bank";

test.describe("TC-002 attempt composition @regression", () => {
  for (const track of TRACKS) {
    test(`${track.name}: 20 questions = 10 common + 10 ${track.id}`, async ({ api }) => {
      const attempt = await api.freshAttempt(track.id);
      const qs = attempt.questions;
      expect(qs).toHaveLength(20);
      expect(qs.map((q) => q.position)).toEqual(Array.from({ length: 20 }, (_, i) => i + 1));
      expect(new Set(qs.map((q) => q.question_id)).size).toBe(20);
      expect(qs.slice(0, 10).every((q) => q.category === "common")).toBe(true);
      expect(qs.slice(10).every((q) => q.category === "role_specific")).toBe(true);
      // Fixed order (DEC-05) matches the seed codes; track questions belong to this track only.
      const prefix = { manual_qa: "PH-MAN", automation_qa: "PH-AUT", sdet: "PH-SDT", qa_lead: "PH-LEAD" }[track.id];
      expect(qs.slice(0, 10).map((q) => seedQuestion(q.prompt).code)).toEqual(
        Array.from({ length: 10 }, (_, i) => `PH-COM-${String(i + 1).padStart(2, "0")}`),
      );
      expect(qs.slice(10).every((q) => seedQuestion(q.prompt).code.startsWith(prefix))).toBe(true);
      expect(qs.every((q) => q.options.map((o) => o.id).join("") === "ABCD")).toBe(true);
    });
  }
});
