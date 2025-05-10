import axios, { AxiosRequestHeaders, Method } from "axios";

interface apiConnectorInterface {
  method: Method;
  url: string;
  bodyData?: any;
  headers?: AxiosRequestHeaders;
  params?: Record<string, any>;
}

const axiosInstance = axios.create({});

export const apiConnector = ({
  method,
  url,
  bodyData,
  headers,
  params,
}: apiConnectorInterface) => {
  return axiosInstance({
    method,
    url,
    data: bodyData ?? null,
    headers,
    params,
  });
};
