import { useState } from "react";
import { RectButton } from "../../../../../components/buttons";
import { Title } from "../../../../../components/Title";
import { TextInput } from "../../inputs";

export function LoginForm() {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");

  const onUserNameChange: React.ChangeEventHandler<HTMLInputElement> = (e) =>
    setUserName(e.target.value);

  const onPasswordChange: React.ChangeEventHandler<HTMLInputElement> = (e) =>
    setPassword(e.target.value);

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
          label={"Password"}
          value={password}
          onChange={onPasswordChange}
          error={""}
          disabled={false}
          type="password"
        />
      </div>
      <RectButton
        title={"LOGIN"}
        onClick={() => {}}
        disabled={false}
        loading={false}
      />
    </>
  );
}
