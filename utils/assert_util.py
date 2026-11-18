# -*- coding: utf-8 -*-
"""断言封装：统一失败信息，避免每个用例重复写 assert 细节。"""


class AssertUtil:

    @staticmethod
    def status_code(resp, expect: int):
        assert resp.status_code == expect, (
            f"状态码不符：期望 {expect}，实际 {resp.status_code}，"
            f"响应体 {resp.text[:300]}"
        )

    @staticmethod
    def json_field(resp, field: str, expect):
        body = resp.json()
        actual = body.get(field)
        assert actual == expect, f"字段 {field} 不符：期望 {expect!r}，实际 {actual!r}"

    @staticmethod
    def json_field_not_empty(resp, field: str):
        body = resp.json()
        actual = body.get(field)
        assert actual, f"字段 {field} 为空，响应体 {body}"

    @staticmethod
    def response_time(resp, limit_ms: int):
        cost = resp.elapsed.total_seconds() * 1000
        assert cost < limit_ms, f"响应耗时 {cost:.0f}ms 超过阈值 {limit_ms}ms"
