import { useState } from "react";
import { RectButton } from "../../../../../components/buttons";
import { TextInput } from "../../inputs";

export function LoginForm() {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");

  const onUserNameChange: React.ChangeEventHandler<HTMLInputElement> = (e) =>
    setUserName(e.target.value);

  const onPasswordChange: React.ChangeEventHandler<HTMLInputElement> = (e) =>
    setPassword(e.target.value);

  return (
    <div className="max-w-md bg-white border border-gray-200 rounded-lg shadow-md dark:bg-gray-800 dark:border-gray-700 px-10 py-5 ">
      <h1 className="text-3xl text-center font-bold font-sans mb-8 text-gray-600">
        Login
      </h1>
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
    </div>
  );
}
