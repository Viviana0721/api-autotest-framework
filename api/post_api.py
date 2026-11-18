# -*- coding: utf-8 -*-
"""资源接口封装：只写业务语义，不写 HTTP 细节。"""
from api.base_api import BaseApi


class PostApi(BaseApi):
    """以 posts 资源为例，对应实习中的「订单」模块。"""

    def list_posts(self, **params):
        return self.get("/posts", params=params)

    def get_post(self, post_id: int):
        return self.get(f"/posts/{post_id}")

    def create_post(self, payload: dict):
        return self.post("/posts", json=payload)

    def update_post(self, post_id: int, payload: dict):
        return self.put(f"/posts/{post_id}", json=payload)

    def delete_post(self, post_id: int):
        return self.delete(f"/posts/{post_id}")
