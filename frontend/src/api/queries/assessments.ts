import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../client";
import { unwrap } from "../errors";
import type { Attempt } from "../types";
import { queryKeys } from "./keys";

export function useTracks() {
  return useQuery({
    queryKey: queryKeys.tracks,
    queryFn: async () => unwrap(await api.GET("/api/v1/assessment-tracks")),
  });
}

export function useAttempts(status?: "in_progress" | "submitted") {
  return useQuery({
    queryKey: queryKeys.attempts(status),
    queryFn: async () =>
      unwrap(await api.GET("/api/v1/attempts", { params: { query: { status, limit: 50 } } })),
  });
}

export function useAttempt(id: string) {
  return useQuery({
    queryKey: queryKeys.attempt(id),
    queryFn: async () =>
      unwrap(await api.GET("/api/v1/attempts/{attempt_id}", { params: { path: { attempt_id: id } } })),
  });
}

export function useReview(id: string) {
  return useQuery({
    queryKey: queryKeys.review(id),
    queryFn: async () =>
      unwrap(
        await api.GET("/api/v1/attempts/{attempt_id}/review", { params: { path: { attempt_id: id } } }),
      ),
    staleTime: 0,
  });
}

export function useResults(id: string) {
  return useQuery({
    queryKey: queryKeys.results(id),
    queryFn: async () =>
      unwrap(
        await api.GET("/api/v1/attempts/{attempt_id}/results", { params: { path: { attempt_id: id } } }),
      ),
    staleTime: Infinity, // submitted results are immutable
  });
}

export function useStartAttempt() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (trackId: string) =>
      unwrap(await api.POST("/api/v1/attempts", { body: { track_id: trackId } })),
    onSuccess: (attempt) => {
      qc.setQueryData(queryKeys.attempt(attempt.id), attempt);
      qc.invalidateQueries({ queryKey: ["attempts"] });
      qc.invalidateQueries({ queryKey: queryKeys.dashboard });
    },
  });
}

/** Saves an answer with an optimistic cache update and rollback on failure. */
export function useSaveAnswer(attemptId: string) {
  const qc = useQueryClient();
  const key = queryKeys.attempt(attemptId);
  return useMutation({
    mutationFn: async (v: { questionId: string; optionId: string }) =>
      unwrap(
        await api.PUT("/api/v1/attempts/{attempt_id}/answers/{question_id}", {
          params: { path: { attempt_id: attemptId, question_id: v.questionId } },
          body: { selected_option_id: v.optionId },
        }),
      ),
    onMutate: async (v) => {
      await qc.cancelQueries({ queryKey: key });
      const previous = qc.getQueryData<Attempt>(key);
      if (previous) {
        const questions = previous.questions.map((q) =>
          q.question_id === v.questionId ? { ...q, selected_option_id: v.optionId } : q,
        );
        qc.setQueryData<Attempt>(key, {
          ...previous,
          questions,
          answered_count: questions.filter((q) => q.selected_option_id).length,
        });
      }
      return { previous };
    },
    onError: (_e, _v, ctx) => {
      if (ctx?.previous) qc.setQueryData(key, ctx.previous);
    },
    onSettled: () => {
      qc.invalidateQueries({ queryKey: queryKeys.review(attemptId) });
      qc.invalidateQueries({ queryKey: ["attempts"] });
    },
  });
}

export function useSubmitAttempt(attemptId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async () =>
      unwrap(
        await api.POST("/api/v1/attempts/{attempt_id}/submit", {
          params: { path: { attempt_id: attemptId } },
        }),
      ),
    onSuccess: (result) => {
      qc.setQueryData(queryKeys.results(attemptId), result);
      qc.invalidateQueries({ queryKey: queryKeys.attempt(attemptId) });
      qc.invalidateQueries({ queryKey: ["attempts"] });
      qc.invalidateQueries({ queryKey: queryKeys.dashboard });
    },
  });
}

export function useAdminCompetencies() {
  return useQuery({
    queryKey: queryKeys.adminCompetencies,
    queryFn: async () => unwrap(await api.GET("/api/v1/admin/competencies")),
  });
}

export function useDashboardSummary() {
  return useQuery({
    queryKey: queryKeys.dashboard,
    queryFn: async () => unwrap(await api.GET("/api/v1/dashboard/summary")),
    staleTime: 0,
  });
}

export function useAdminDashboardSummary() {
  return useQuery({
    queryKey: queryKeys.adminDashboard,
    queryFn: async () => unwrap(await api.GET("/api/v1/admin/dashboard/summary")),
  });
}
