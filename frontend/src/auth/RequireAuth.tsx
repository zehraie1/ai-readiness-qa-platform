import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router";
import { useMe } from "@/api/queries/auth";
import { PageSkeleton } from "@/components/States";

type Role = "participant" | "administrator";

/** UX guard only: the API enforces every permission server-side. */
export function RequireAuth({ role, children }: { role?: Role; children: ReactNode }) {
  const { data: me, isPending } = useMe();
  const location = useLocation();
  if (isPending) return <PageSkeleton />;
  if (!me) {
    const next = encodeURIComponent(location.pathname + location.search);
    return <Navigate to={`/login?next=${next}`} replace />;
  }
  if (role && me.role !== role) return <Navigate to="/forbidden" replace />;
  return <>{children}</>;
}

export function homeFor(role: string | undefined) {
  return role === "administrator" ? "/admin" : "/";
}
