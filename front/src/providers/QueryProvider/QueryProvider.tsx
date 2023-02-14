import React, { PropsWithChildren } from "react";
import { QueryClientProvider } from "react-query";
import { queryClient } from "../../queryClient";

interface QueryProviderProps extends PropsWithChildren {}

export function QueryProvider({ children }: QueryProviderProps) {
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}
