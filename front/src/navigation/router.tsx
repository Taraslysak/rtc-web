import { createBrowserRouter } from "react-router-dom";
import { Auth } from "../pages/Auth";
import {Intro} from "../pages/Intro";
import { Main } from "../pages/Main";

export const router = createBrowserRouter([

    {
      path: "/auth",
      element: <Auth/>,
    },
    {
      path: "/main",
      element: <Main/>,
    },
    {
      path: "/",
      element: <Intro/>,
    },
  ]);