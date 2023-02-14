import { useState } from "react";
import { useMutation } from "react-query";
import { useNavigate } from "react-router-dom";
import { RectButton } from "../../../../../components/buttons";
import { ErrorMessage } from "../../../../../components/ErrorMessage";
import { Title } from "../../../../../components/Title";
import {
  ApiError,
  AuthService,
  Body_auth_login,
  Token,
} from "../../../../../services";
import { LOCAL_STORAGE_KEY, ROUTE_PATH } from "../../../../../strings";
import { TextInput } from "../../inputs";

export function LoginForm() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const { mutate, isLoading, error } = useMutation<
    Token,
    ApiError,
    Body_auth_login,
    unknown
  >(AuthService.authLogin, {
    onSuccess: (data) => {
      localStorage.setItem(LOCAL_STORAGE_KEY.AUTH_TOKEN, data.access_token);
      navigate(ROUTE_PATH.MAIN);
    },
  });

  const onUserNameChange: React.ChangeEventHandler<HTMLInputElement> = (e) =>
    setEmail(e.target.value);

  const onPasswordChange: React.ChangeEventHandler<HTMLInputElement> = (e) =>
    setPassword(e.target.value);

  const handleLogin = () => {
    console.log("handleLogin called");

    mutate({ email, password });
  };
  console.log({ error }, error?.body);

  return (
    <>
      <Title text="Login" />
      <div className="space-y-4 mb-10">
        <TextInput
          label={"Email"}
          value={email}
          onChange={onUserNameChange}
          error={""}
          disabled={false}
        />
        <TextInput
          label={"Password"}
          value={password}
          onChange={onPasswordChange}
          error={""}
          disabled={false}
          type="password"
        />
      </div>
      {error && <ErrorMessage message={error.body.detail} />}
      <RectButton
        title={"LOGIN"}
        onClick={handleLogin}
        disabled={isLoading}
        loading={isLoading}
      />
    </>
  );
}
