# -*- coding: utf-8 -*-
"""统一请求入口：集中处理 base_url 拼接、超时、日志。

用例层只关心「调哪个接口、传什么参、断什么结果」，不关心怎么发请求。
"""
import logging
import time

import requests

logger = logging.getLogger("api")


class BaseApi:
    def __init__(self, base_url: str, timeout: int = 10, headers: dict | None = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)

        logger.info("请求 → %s %s | params=%s | body=%s",
                    method.upper(), url, kwargs.get("params"), kwargs.get("json"))
        start = time.perf_counter()
        resp = self.session.request(method.upper(), url, **kwargs)
        cost = (time.perf_counter() - start) * 1000

        logger.info("响应 ← %s | %.0fms | %s", resp.status_code, cost, resp.text[:200])
        return resp

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.request("DELETE", path, **kwargs)
