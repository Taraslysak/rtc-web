import { OpenAPI } from "./services/core/OpenAPI";
import { LOCAL_STORAGE_KEY } from "./strings";

export function configureApiService() {
  const getApiToken = async (): Promise<string> => {
    console.log(localStorage.getItem(LOCAL_STORAGE_KEY.AUTH_TOKEN));

    return localStorage.getItem(LOCAL_STORAGE_KEY.AUTH_TOKEN) ?? "";
  };
  OpenAPI.TOKEN = getApiToken;
}
