import { Background } from "../../components/layout/Background/Background";
import { Header } from "../../components/layout/Header";
import { useAuthCheck } from "../../customHooks/useAuthCheck";

export function Main() {
  useAuthCheck();
  return (
    <>
      <Background>
        <Header />

        <div className="flex-auto"></div>
      </Background>
    </>
  );
}
