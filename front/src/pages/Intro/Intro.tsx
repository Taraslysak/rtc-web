import { useEffect } from "react";
import { useQuery } from "react-query";
import { useNavigate } from "react-router-dom";
import { useAuthCheck } from "../../customHooks/useAuthCheck";
import { AuthService } from "../../services";
import { LOCAL_STORAGE_KEY, ROUTE_PATH } from "../../strings";

export function Intro() {
  useAuthCheck();

  return <div>Intro</div>;
}
