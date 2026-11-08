import { type APIRequestContext, type APIResponse, expect, request } from "@playwright/test";
import { API_BASE_URL, BASE_URL } from "./env";
import { correctOptionFor, wrongOptionFor } from "../data/bank";

// Request contexts created inside a test inherit the project's storageState; start from empty.
const EMPTY = { cookies: [], origins: [] };

export interface AttemptQuestion {
  question_id: string;
  position: number;
  category: "common" | "role_specific";
  prompt: string;
  options: { id: string; text: string }[];
  selected_option_id: string | null;
}
export interface Attempt {
  id: string;
  track_id: string;
  status: string;
  questions: AttemptQuestion[];
  [k: string]: unknown;
}

/** Thin typed wrapper over the REST API for test setup and API specs. */
export class ApiClient {
  constructor(readonly ctx: APIRequestContext) {}

  static async login(email: string, password: string): Promise<ApiClient> {
    const ctx = await request.newContext({ baseURL: API_BASE_URL, extraHTTPHeaders: { Origin: BASE_URL }, storageState: EMPTY });
    const res = await ctx.post("/api/v1/auth/login", { data: { email, password } });
    expect(res.status(), `login ${email}`).toBe(200);
    return new ApiClient(ctx);
  }

  static async anonymous(): Promise<ApiClient> {
    return new ApiClient(
      await request.newContext({ baseURL: API_BASE_URL, extraHTTPHeaders: { Origin: BASE_URL }, storageState: EMPTY }),
    );
  }

  get = (path: string) => this.ctx.get(`/api/v1${path}`);
  post = (path: string, data?: unknown) => this.ctx.post(`/api/v1${path}`, { data });
  put = (path: string, data?: unknown) => this.ctx.put(`/api/v1${path}`, { data });

  async json<T>(res: Promise<APIResponse> | APIResponse, status = 200): Promise<T> {
    const r = await res;
    expect(r.status(), await r.text()).toBe(status);
    return (await r.json()) as T;
  }

  async startAttempt(track: string): Promise<Attempt> {
    const r = await this.post("/attempts", { track_id: track });
    expect([200, 201]).toContain(r.status());
    return (await r.json()) as Attempt;
  }

  answer(attemptId: string, questionId: string, option: string) {
    return this.put(`/attempts/${attemptId}/answers/${questionId}`, { selected_option_id: option });
  }

  /** Answer every question; correct only at `correctPositions` (default: all correct). */
  async answerAll(attempt: Attempt, correctPositions?: Set<number>) {
    for (const q of attempt.questions) {
      const correct = !correctPositions || correctPositions.has(q.position);
      const option = correct ? correctOptionFor(q.prompt) : wrongOptionFor(q.prompt);
      const r = await this.answer(attempt.id, q.question_id, option);
      expect(r.status(), await r.text()).toBe(200);
    }
  }

  /** Finish any leftover in-progress attempt for the track, then start a fresh one. */
  async freshAttempt(track: string): Promise<Attempt> {
    const existing = await this.startAttempt(track);
    if (existing.questions.some((q) => q.selected_option_id !== null)) {
      await this.answerAll(existing);
      await this.json(this.post(`/attempts/${existing.id}/submit`));
      return this.startAttempt(track);
    }
    return existing;
  }

  dispose = () => this.ctx.dispose();
}
