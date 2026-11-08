import { createBrowserRouter, type RouteObject } from "react-router";
import { RequireAuth } from "@/auth/RequireAuth";
import { AppShell } from "@/components/AppShell";
import { AdminHomePage } from "@/pages/admin/AdminHomePage";
import { DashboardPage } from "@/pages/DashboardPage";
import { ForbiddenPage } from "@/pages/ForbiddenPage";
import { LoginPage } from "@/pages/LoginPage";
import { NotFoundPage } from "@/pages/NotFoundPage";
import { QuestionPage } from "@/pages/QuestionPage";
import { ResultsPage } from "@/pages/ResultsPage";
import { ReviewPage } from "@/pages/ReviewPage";
import { TracksPage } from "@/pages/TracksPage";

const participant = (el: React.ReactNode) => <RequireAuth role="participant">{el}</RequireAuth>;

export const routes: RouteObject[] = [
  { path: "/login", element: <LoginPage /> },
  {
    element: (
      <RequireAuth>
        <AppShell />
      </RequireAuth>
    ),
    children: [
      { path: "/", element: participant(<DashboardPage />) },
      { path: "/assessments/tracks", element: participant(<TracksPage />) },
      { path: "/attempts/:id/questions/:position", element: participant(<QuestionPage />) },
      { path: "/attempts/:id/review", element: participant(<ReviewPage />) },
      { path: "/attempts/:id/results", element: participant(<ResultsPage />) },
      { path: "/admin", element: <RequireAuth role="administrator"><AdminHomePage /></RequireAuth> },
      { path: "/forbidden", element: <ForbiddenPage /> },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
];

export const router = createBrowserRouter(routes);
