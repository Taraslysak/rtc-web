import { PropsWithChildren } from "react";

interface Card extends PropsWithChildren {}

export function Card({ children }: Card) {
  return (
    <div className="max-w-md bg-white border border-gray-200 rounded-lg shadow-md dark:bg-gray-800 dark:border-gray-700 px-10 py-5">
      {children}
    </div>
  );
}
