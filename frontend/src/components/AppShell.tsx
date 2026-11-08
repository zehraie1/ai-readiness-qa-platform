import { ClipboardList, LayoutDashboard, LogOut, Menu, ShieldCheck, X } from "lucide-react";
import { useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router";
import { useLogout, useMe } from "@/api/queries/auth";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const PARTICIPANT_NAV = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/assessments/tracks", label: "Assessments", icon: ClipboardList, end: false },
];
const ADMIN_NAV = [{ to: "/admin", label: "Administration", icon: ShieldCheck, end: false }];

export function AppShell() {
  const { data: me } = useMe();
  const logout = useLogout();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const nav = me?.role === "administrator" ? ADMIN_NAV : PARTICIPANT_NAV;

  return (
    <div className="min-h-screen md:grid md:grid-cols-[240px_1fr]">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-2 focus:top-2 focus:z-50 focus:rounded focus:bg-surface focus:px-3 focus:py-2"
      >
        Skip to main content
      </a>
      <header className="flex items-center justify-between bg-navy-900 px-4 py-3 text-white md:hidden">
        <span className="font-semibold">AI Readiness</span>
        <Button
          variant="ghost"
          size="icon"
          className="text-white hover:bg-navy-800"
          aria-expanded={open}
          aria-controls="primary-nav"
          onClick={() => setOpen((o) => !o)}
        >
          {open ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
          <span className="sr-only">{open ? "Close navigation" : "Open navigation"}</span>
        </Button>
      </header>
      <aside
        id="primary-nav"
        className={cn("bg-navy-900 text-white md:flex md:flex-col", open ? "flex flex-col" : "hidden")}
      >
        <div className="hidden px-6 py-5 md:block">
          <p className="text-lg font-semibold">AI Readiness</p>
          <p className="text-xs text-white/70">Quality Engineering Assessment</p>
        </div>
        <nav aria-label="Primary" className="flex-1 px-3 py-2">
          <ul className="space-y-1">
            {nav.map(({ to, label, icon: Icon, end }) => (
              <li key={to}>
                <NavLink
                  to={to}
                  end={end}
                  onClick={() => setOpen(false)}
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 rounded-[var(--radius-control)] px-3 py-2 text-sm text-white/85 hover:bg-navy-800 hover:text-white",
                      isActive && "bg-navy-800 font-semibold text-white",
                    )
                  }
                >
                  <Icon aria-hidden="true" className="size-4" />
                  {label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <div className="border-t border-white/10 px-6 py-4 text-sm">
          <p className="truncate font-medium">{me?.display_name}</p>
          <p className="truncate text-xs text-white/70">{me?.email}</p>
          <Button
            variant="ghost"
            size="sm"
            className="mt-3 -ml-3 text-white hover:bg-navy-800"
            onClick={() => logout.mutate(undefined, { onSettled: () => navigate("/login") })}
          >
            <LogOut aria-hidden="true" /> Sign out
          </Button>
        </div>
      </aside>
      <main id="main" tabIndex={-1} className="mx-auto w-full max-w-5xl px-4 py-6 md:px-8 md:py-10">
        <Outlet />
      </main>
    </div>
  );
}
