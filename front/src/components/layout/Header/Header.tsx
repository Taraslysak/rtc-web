import { useMutation } from "react-query";
import { useNavigate } from "react-router-dom";
import { AuthService } from "../../../services";
import { LOCAL_STORAGE_KEY, ROUTE_PATH } from "../../../strings";

export function Header() {
  const navigate = useNavigate();
  const { mutate, isLoading } = useMutation(AuthService.authLogout, {
    onSuccess: () => {
      localStorage.removeItem(LOCAL_STORAGE_KEY.AUTH_TOKEN);
      navigate(ROUTE_PATH.INTRO);
    },
  });
  const handleLogout = () => {
    mutate();
  };
  return (
    <div>
      <nav className="flex items-center justify-between flex-wrap bg-fiord-900 p-6">
        <div className="flex items-center flex-shrink-0 text-white mr-6">
          <svg
            className="fill-current h-8 w-8 mr-2"
            width="54"
            height="54"
            viewBox="0 0 54 54"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M13.5 22.1c1.8-7.2 6.3-10.8 13.5-10.8 10.8 0 12.15 8.1 17.55 9.45 3.6.9 6.75-.45 9.45-4.05-1.8 7.2-6.3 10.8-13.5 10.8-10.8 0-12.15-8.1-17.55-9.45-3.6-.9-6.75.45-9.45 4.05zM0 38.3c1.8-7.2 6.3-10.8 13.5-10.8 10.8 0 12.15 8.1 17.55 9.45 3.6.9 6.75-.45 9.45-4.05-1.8 7.2-6.3 10.8-13.5 10.8-10.8 0-12.15-8.1-17.55-9.45-3.6-.9-6.75.45-9.45 4.05z" />
          </svg>
          <span className="font-semibold text-xl tracking-tight">
            SimpleRTC
          </span>
        </div>
        <button
          className="font-semibold text-xl tracking-tight text-white hover:text-fiord-200 hover:underline active:text-fiord-400"
          onClick={handleLogout}
          disabled={isLoading}
        >
          Logout
        </button>
      </nav>
    </div>
  );
}
