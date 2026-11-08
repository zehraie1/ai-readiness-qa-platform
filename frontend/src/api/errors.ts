export interface ErrorEnvelope {
  code: string;
  message: string;
  details?: unknown;
  request_id: string;
}

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details: unknown;
  readonly requestId: string | null;

  constructor(status: number, envelope: Partial<ErrorEnvelope> | undefined) {
    super(envelope?.message ?? "Something went wrong. Please try again.");
    this.name = "ApiError";
    this.status = status;
    this.code = envelope?.code ?? "UNKNOWN_ERROR";
    this.details = envelope?.details;
    this.requestId = envelope?.request_id ?? null;
  }
}

/** Normalise an openapi-fetch result into data-or-throw. */
export function unwrap<T>(result: { data?: T; error?: unknown; response: Response }): T {
  if (result.error !== undefined || !result.response.ok) {
    throw new ApiError(result.response.status, result.error as Partial<ErrorEnvelope>);
  }
  return result.data as T;
}

export function isApiError(e: unknown, status?: number): e is ApiError {
  return e instanceof ApiError && (status === undefined || e.status === status);
}
