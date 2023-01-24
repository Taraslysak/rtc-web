import { RouterProvider } from "react-router-dom";
import { router } from "./navigation";

function App() {
  return (
    <div className="bg-pink-300">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
