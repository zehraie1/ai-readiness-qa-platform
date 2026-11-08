import { MutationCache, QueryCache, QueryClient } from "@tanstack/react-query";
import { isApiError } from "./errors";
import { queryKeys } from "./queries/keys";

function onAuthError(error: unknown) {
  // Expired/revoked session: clearing "me" makes the route guard redirect to /login.
  if (isApiError(error, 401)) queryClient.setQueryData(queryKeys.me, null);
}

export const queryClient = new QueryClient({
  queryCache: new QueryCache({ onError: onAuthError }),
  mutationCache: new MutationCache({ onError: onAuthError }),
  defaultOptions: {
    queries: {
      retry: (count, error) => !isApiError(error) && count < 2,
      refetchOnWindowFocus: false,
      staleTime: 15_000,
    },
  },
});
