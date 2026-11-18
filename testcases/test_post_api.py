# -*- coding: utf-8 -*-
"""posts 资源接口测试。

用例分层：
- 正向：正常查询、创建、更新、删除
- 反向：不存在的资源、必填字段缺失
- 数据驱动：查询场景来自 data/post_cases.yaml
"""
import os

import pytest
import yaml

CASE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "post_cases.yaml")
with open(CASE_FILE, encoding="utf-8") as f:
    QUERY_CASES = yaml.safe_load(f)


class TestPostQuery:

    @pytest.mark.parametrize("case", QUERY_CASES, ids=[c["name"] for c in QUERY_CASES])
    def test_query_by_id(self, post_api, expect, case):
        resp = post_api.get_post(case["post_id"])
        expect.status_code(resp, case["expect_status"])
        if case.get("expect_id"):
            expect.json_field(resp, "id", case["expect_id"])
            expect.json_field_not_empty(resp, "title")
        expect.response_time(resp, 3000)

    def test_list_posts_with_limit(self, post_api, expect):
        resp = post_api.list_posts(_limit=5)
        expect.status_code(resp, 200)
        assert len(resp.json()) == 5, "limit 参数未生效"


class TestPostWrite:

    def test_create_post(self, post_api, expect):
        payload = {"title": "回归测试用例", "body": "自动化创建", "userId": 1}
        resp = post_api.create_post(payload)
        expect.status_code(resp, 201)
        expect.json_field(resp, "title", payload["title"])

    def test_update_post(self, post_api, expect):
        payload = {"id": 1, "title": "更新后的标题", "body": "内容", "userId": 1}
        resp = post_api.update_post(1, payload)
        expect.status_code(resp, 200)
        expect.json_field(resp, "title", payload["title"])

    def test_delete_post(self, post_api, expect):
        resp = post_api.delete_post(1)
        expect.status_code(resp, 200)

    @pytest.mark.xfail(reason="服务端未做入参校验：缺少 title 仍返回 201，应返回 400", strict=True)
    def test_create_post_missing_required_field(self, post_api):
        resp = post_api.create_post({"body": "只有内容没有标题", "userId": 1})
        assert resp.status_code == 400, f"缺少必填字段应拒绝，实际 {resp.status_code}"
