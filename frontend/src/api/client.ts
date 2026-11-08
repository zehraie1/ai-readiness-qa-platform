import createClient from "openapi-fetch";
import type { paths } from "./schema";

/** Typed API client. Same-origin by default (Vite proxies /api in development). */
export const api = createClient<paths>({
  baseUrl: import.meta.env.VITE_API_BASE_URL ?? "",
  credentials: "include",
  headers: { Accept: "application/json" },
});
