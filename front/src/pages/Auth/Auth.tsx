import { useState } from "react";
import { Background } from "../../components/layout/Background/Background";
import { Card } from "../../components/layout/Card";
import { LoginForm } from "./components/forms/LoginForm";
import { RegisterForm } from "./components/forms/RegisterForm";

type AuthProps = {};

export function Auth({}: AuthProps) {
  const [isLogin, setIsLogin] = useState<boolean>(true);
  const toggleIsLogin = () => {
    setIsLogin((prev) => !prev);
  };

  const handleRegister = () => {
    setIsLogin(true);
  };

  return (
    <Background>
      <div className="grid content-center justify-center">
        <Card>
          {isLogin ? (
            <LoginForm />
          ) : (
            <RegisterForm onRegister={handleRegister} />
          )}
          <button
            className="text-blue-700 hover:text-blue-400 underline cursor-pointer active:text-blue-100"
            onClick={toggleIsLogin}
          >
            {isLogin ? "Register" : "Login"}
          </button>
        </Card>
      </div>
    </Background>
  );
}
