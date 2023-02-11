import { RouterProvider } from "react-router-dom";
import { Background } from "./components/layout/Background/Background";
import { router } from "./navigation";

function App() {
  return (
    <div className="flex w-full h-full">
      <RouterProvider router={router} />;
    </div>
  );
}

export default App;
