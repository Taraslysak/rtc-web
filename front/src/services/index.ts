/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export { ApiError } from './core/ApiError';
export { CancelablePromise, CancelError } from './core/CancelablePromise';
export { OpenAPI } from './core/OpenAPI';
export type { OpenAPIConfig } from './core/OpenAPI';

export type { Body_auth_login } from './models/Body_auth_login';
export type { HTTPValidationError } from './models/HTTPValidationError';
export type { Token } from './models/Token';
export type { UserRegister } from './models/UserRegister';
export type { ValidationError } from './models/ValidationError';

export { AuthService } from './services/AuthService';
export { MainService } from './services/MainService';
export { WsService } from './services/WsService';
