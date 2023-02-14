import { useState } from "react";
import { useMutation } from "react-query";
import { RectButton } from "../../../../../components/buttons";
import { ErrorMessage } from "../../../../../components/ErrorMessage";
import { Title } from "../../../../../components/Title";
import { ApiError, AuthService, UserRegister } from "../../../../../services";
import { TextInput } from "../../inputs";

interface IRegisterFormProps {
  onRegister: () => void;
}

export function RegisterForm({ onRegister }: IRegisterFormProps) {
  const { mutate, error, isLoading } = useMutation<
    typeof AuthService.authRegister,
    ApiError,
    UserRegister,
    unknown
  >(AuthService.authRegister, {
    onSuccess: () => {
      onRegister();
    },
  });
  const [userName, setUserName] = useState("");
  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const onUserNameChange: React.ChangeEventHandler<HTMLInputElement> = (e) =>
    setUserName(e.target.value);

  const onEmailChange: React.ChangeEventHandler<HTMLInputElement> = (e) =>
    setEmail(e.target.value);

  const onPasswordChange: React.ChangeEventHandler<HTMLInputElement> = (e) =>
    setPassword(e.target.value);

  const onConfirmPasswordChange: React.ChangeEventHandler<HTMLInputElement> = (
    e
  ) => setConfirmPassword(e.target.value);

  const handleRegister = () => {
    if (!userName || !email || !password || password !== confirmPassword) {
      return;
    }
    mutate({ username: userName, email, password });
  };

  return (
    <>
      <Title text="Login" />
      <div className="space-y-4 mb-10">
        <TextInput
          label={"Username"}
          value={userName}
          onChange={onUserNameChange}
          error={""}
          disabled={false}
        />
        <TextInput
          label={"Email"}
          value={email}
          onChange={onEmailChange}
          error={""}
          disabled={false}
          type="email"
        />
        <div className="h-1"></div>
        <TextInput
          label={"Password"}
          value={password}
          onChange={onPasswordChange}
          error={""}
          disabled={false}
          type="password"
        />
        <TextInput
          label={"Confirm Password"}
          value={confirmPassword}
          onChange={onConfirmPasswordChange}
          error={""}
          disabled={false}
          type="password"
        />
      </div>
      {error && <ErrorMessage message={error.body?.detail} />}
      <RectButton
        title={"REGISTER"}
        onClick={handleRegister}
        disabled={isLoading}
        loading={isLoading}
      />
    </>
  );
}
