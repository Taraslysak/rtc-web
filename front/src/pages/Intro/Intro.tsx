import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export function Intro() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("AUTH_TOKEN");
    navigate(token ? "main" : "auth");
  }, []);

  return <div>Intro</div>;
}
