import React, { PropsWithChildren } from "react";

interface Props extends PropsWithChildren {}

export function Background({ children }: Props) {
  return (
    <div className="h-screen w-screen bg-gradient-to-tl from-fiord-700  to-fiord-600 grid ">
      {children}
    </div>
  );
}
