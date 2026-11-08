import type { AttemptQuestion, Result } from "@/api/types";

export const question: AttemptQuestion = {
  question_id: "11111111-1111-1111-1111-111111111111",
  position: 3,
  category: "common",
  prompt: "[DRAFT] Which technique checks metamorphic relations?",
  options: [
    { id: "A", text: "Metamorphic testing" },
    { id: "B", text: "Smoke testing" },
    { id: "C", text: "Load testing" },
    { id: "D", text: "Static analysis" },
  ],
  selected_option_id: null,
};

export const result: Result = {
  attempt_id: "22222222-2222-2222-2222-222222222222",
  track_id: "sdet",
  track_name: "SDET",
  submitted_at: "2026-11-08T10:00:00Z",
  overall_score: 45,
  max_score: 100,
  correct_count: 9,
  total_questions: 20,
  common_score: 30,
  role_specific_score: 15,
  readiness_band: { code: "developing", label: "Developing", min: 40, max: 59 },
  competencies: [
    { code: "PH_A", label: "Data quality and bias", correct: 1, total: 4, percentage: 25, assessed: true },
    { code: "PH_B", label: "Testing AI-based systems", correct: 5, total: 7, percentage: 71, assessed: true },
    { code: "PH_C", label: "Quality leadership", correct: 0, total: 0, percentage: null, assessed: false },
  ],
  recommendations: [
    { position: 1, competency_code: "PH_A", competency_label: "Data quality and bias", title: "Build data checks", body: "Body" },
  ],
  versions: { question_bank: "placeholder-v0", scoring_policy: "v1-simple", recommendation_rules: "placeholder-rec-v0" },
  content_provenance: "placeholder_unverified",
  disclaimer: "Internal classification.",
};
