import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { createMemoryRouter, RouterProvider } from "react-router";
import { beforeEach, describe, expect, it, vi } from "vitest";

const GET = vi.fn();
const POST = vi.fn();
vi.mock("@/api/client", () => ({ api: { GET: (...a: unknown[]) => GET(...a), POST: (...a: unknown[]) => POST(...a) } }));

const { LoginPage } = await import("./LoginPage");

function renderLogin() {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const router = createMemoryRouter(
    [
      { path: "/login", element: <LoginPage /> },
      { path: "/", element: <h1>Dashboard home</h1> },
    ],
    { initialEntries: ["/login"] },
  );
  render(
    <QueryClientProvider client={qc}>
      <RouterProvider router={router} />
    </QueryClientProvider>,
  );
}

const unauthenticated = { error: { code: "UNAUTHENTICATED", message: "x", request_id: "r" }, response: new Response(null, { status: 401 }) };

describe("LoginPage", () => {
  beforeEach(() => {
    GET.mockReset().mockResolvedValue(unauthenticated);
    POST.mockReset();
  });

  it("validates fields and ties errors to inputs", async () => {
    const user = userEvent.setup();
    renderLogin();
    await user.click(await screen.findByRole("button", { name: "Sign in" }));
    const email = screen.getByLabelText("Email");
    expect(email).toHaveAttribute("aria-invalid", "true");
    expect(email).toHaveAccessibleDescription("Enter your email address.");
    expect(screen.getByLabelText("Password")).toHaveAccessibleDescription("Enter your password.");
    expect(POST).not.toHaveBeenCalled();
  });

  it("shows a generic message for invalid credentials", async () => {
    POST.mockResolvedValue({ error: { code: "INVALID_CREDENTIALS", message: "x", request_id: "r" }, response: new Response(null, { status: 401 }) });
    const user = userEvent.setup();
    renderLogin();
    await user.type(await screen.findByLabelText("Email"), "someone@example.com");
    await user.type(screen.getByLabelText("Password"), "wrong");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Email or password is incorrect.");
  });

  it("redirects a participant home after sign-in", async () => {
    POST.mockResolvedValue({
      data: { id: "u", email: "p@example.com", display_name: "P", role: "participant", permissions: [] },
      response: new Response(null, { status: 200 }),
    });
    const user = userEvent.setup();
    renderLogin();
    await user.type(await screen.findByLabelText("Email"), "p@example.com");
    await user.type(screen.getByLabelText("Password"), "pw");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    expect(await screen.findByRole("heading", { name: "Dashboard home" })).toBeInTheDocument();
  });
});
