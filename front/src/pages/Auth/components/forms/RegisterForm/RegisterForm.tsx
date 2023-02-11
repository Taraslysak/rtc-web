import { useState } from "react";
import { RectButton } from "../../../../../components/buttons";
import { Title } from "../../../../../components/Title";
import { TextInput } from "../../inputs";

export function RegisterForm() {
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
      <RectButton
        title={"REGISTER"}
        onClick={() => {}}
        disabled={false}
        loading={false}
      />
    </>
  );
}
