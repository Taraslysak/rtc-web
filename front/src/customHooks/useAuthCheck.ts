import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { LOCAL_STORAGE_KEY, ROUTE_PATH } from "../strings";

export function useAuthCheck() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem(LOCAL_STORAGE_KEY.AUTH_TOKEN);
    navigate(token ? ROUTE_PATH.MAIN : ROUTE_PATH.AUTH);
  }, []);
}
