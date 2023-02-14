/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class WsService {

    /**
     * Get Ws Token
     * @returns any Successful Response
     * @throws ApiError
     */
    public static wsGetWsToken(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/ws/token',
        });
    }

}
