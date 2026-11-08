import { zodResolver } from "@hookform/resolvers/zod";
import { AlertCircle } from "lucide-react";
import { useForm } from "react-hook-form";
import { Navigate, useNavigate, useSearchParams } from "react-router";
import { z } from "zod";
import { isApiError } from "@/api/errors";
import { useLogin, useMe } from "@/api/queries/auth";
import { homeFor } from "@/auth/RequireAuth";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useDocumentTitle } from "@/lib/format";

const schema = z.object({
  email: z.string().trim().min(1, "Enter your email address.").email("Enter a valid email address."),
  password: z.string().min(1, "Enter your password."),
});
type FormValues = z.infer<typeof schema>;

function safeNext(next: string | null) {
  return next && next.startsWith("/") && !next.startsWith("//") ? next : null;
}

export function LoginPage() {
  useDocumentTitle("Sign in");
  const { data: me } = useMe();
  const login = useLogin();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({ resolver: zodResolver(schema) });

  if (me) return <Navigate to={safeNext(params.get("next")) ?? homeFor(me.role)} replace />;

  const onSubmit = (values: FormValues) =>
    login.mutate(values, {
      onSuccess: (user) => navigate(safeNext(params.get("next")) ?? homeFor(user.role), { replace: true }),
    });

  const serverError = login.error
    ? isApiError(login.error, 401)
      ? "Email or password is incorrect."
      : "Sign-in is unavailable right now. Please try again."
    : null;

  return (
    <main id="main" className="flex min-h-screen items-center justify-center bg-canvas px-4">
      <Card className="w-full max-w-md">
        <p className="text-sm font-semibold text-blue-700">AI Readiness Assessment</p>
        <h1 className="mt-1 text-2xl font-semibold">Sign in</h1>
        <p className="mt-1 text-sm text-text-muted">Use the account provided by your administrator.</p>
        <form className="mt-6 space-y-4" noValidate onSubmit={handleSubmit(onSubmit)}>
          {serverError && (
            <Alert tone="danger" role="alert">
              <AlertCircle aria-hidden="true" />
              <p>{serverError}</p>
            </Alert>
          )}
          <div className="space-y-1.5">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              autoComplete="username"
              aria-invalid={errors.email ? true : undefined}
              aria-describedby={errors.email ? "email-error" : undefined}
              {...register("email")}
            />
            {errors.email && (
              <p id="email-error" className="text-sm text-danger">{errors.email.message}</p>
            )}
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              autoComplete="current-password"
              aria-invalid={errors.password ? true : undefined}
              aria-describedby={errors.password ? "password-error" : undefined}
              {...register("password")}
            />
            {errors.password && (
              <p id="password-error" className="text-sm text-danger">{errors.password.message}</p>
            )}
          </div>
          <Button type="submit" className="w-full" disabled={login.isPending}>
            {login.isPending ? "Signing in…" : "Sign in"}
          </Button>
        </form>
      </Card>
    </main>
  );
}
