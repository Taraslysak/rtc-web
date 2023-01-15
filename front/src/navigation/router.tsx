import { createBrowserRouter } from "react-router-dom";
import { Auth } from "../pages/Auth";
import { Intro } from "../pages/Intro";
import { Main } from "../pages/Main";
import { ROUTE_PATH } from "../strings";

export const router = createBrowserRouter([
  {
    path: ROUTE_PATH.AUTH,
    element: <Auth />,
  },
  {
    path: ROUTE_PATH.MAIN,
    element: <Main />,
  },
  {
    path: ROUTE_PATH.INTRO,
    element: <Intro />,
  },
]);
