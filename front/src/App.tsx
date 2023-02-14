import { RouterProvider } from "react-router-dom";
import { router } from "./navigation";
import { QueryProvider } from "./providers/QueryProvider/QueryProvider";

function App() {
  return (
    <div className="flex w-full h-full">
      <QueryProvider>
        <RouterProvider router={router} />;
      </QueryProvider>
    </div>
  );
}

export default App;
