export const queryKeys = {
  me: ["me"] as const,
  tracks: ["tracks"] as const,
  attempts: (status?: string) => ["attempts", status ?? "all"] as const,
  attempt: (id: string) => ["attempt", id] as const,
  review: (id: string) => ["review", id] as const,
  results: (id: string) => ["results", id] as const,
  adminCompetencies: ["admin", "competencies"] as const,
  dashboard: ["dashboard"] as const,
  adminDashboard: ["admin", "dashboard"] as const,
};
